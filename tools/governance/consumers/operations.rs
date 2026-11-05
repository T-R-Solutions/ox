//! Controlled Linux consumers; cooperating writers and direct children only.
use std::{
    fs::{self, OpenOptions},
    io::{self, Read, Write},
    path::{Component, Path, PathBuf},
    process::{Child, Command, Stdio},
    sync::{
        Arc,
        atomic::{AtomicBool, AtomicU64, Ordering},
    },
    thread::{self, JoinHandle},
    time::{Duration, Instant},
};
fn failure(s: &str) -> io::Error {
    io::Error::other(s)
}
pub fn bounded_path(root: &Path, relative: &Path) -> io::Result<PathBuf> {
    if relative.as_os_str().is_empty() {
        return Err(failure("empty path"));
    }
    let root = root.canonicalize()?;
    let mut p = root.clone();
    for c in relative.components() {
        match c {
            Component::Normal(v) => p.push(v),
            _ => return Err(failure("non-normal component")),
        };
        let metadata = fs::symlink_metadata(&p)?;
        if metadata.file_type().is_symlink() {
            return Err(failure("symlink"));
        }
    }
    if !p.canonicalize()?.starts_with(&root) {
        return Err(failure("outside root"));
    }
    Ok(p)
}
struct Lock(PathBuf);
impl Drop for Lock {
    fn drop(&mut self) {
        let _ = fs::remove_file(self.0.join("owner"));
        let _ = fs::remove_dir(&self.0);
    }
}
fn lock(root: &Path) -> io::Result<Lock> {
    let p = root.join(".edit-lock");
    let until = Instant::now() + Duration::from_secs(3);
    loop {
        match fs::create_dir(&p) {
            Ok(()) => {
                let lock = Lock(p);
                fs::write(lock.0.join("owner"), std::process::id().to_string())?;
                return Ok(lock);
            }
            Err(e) if e.kind() == io::ErrorKind::AlreadyExists && Instant::now() < until => {
                thread::sleep(Duration::from_millis(2))
            }
            Err(e) => return Err(e),
        }
    }
}
pub fn edit(root: &Path, relative: &Path, base: &[u8], next: &[u8], crash: bool) -> io::Result<()> {
    let target = bounded_path(root, relative)?;
    let _lock = lock(root)?;
    if fs::read(&target)? != base {
        return Err(failure("conflict"));
    }
    if root.join("journal").exists() || root.join("staged").exists() {
        return Err(failure("recovery required"));
    }
    let mut stage = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(root.join("staged"))?;
    stage.write_all(next)?;
    stage.sync_all()?;
    fs::write(root.join("journal"), b"PREPARED")?;
    if crash {
        std::process::exit(91)
    }
    // Recheck after staging. The lock serializes cooperating writers; external writers remain a conflict risk.
    if fs::read(&target)? != base {
        return Err(failure("conflict after staging"));
    }
    fs::rename(root.join("staged"), &target)?;
    fs::write(root.join("journal"), b"DONE")?;
    Ok(())
}
pub fn recover_after_reap(root: &Path, reaped_pid: u32) -> io::Result<Vec<u8>> {
    let lock = root.join(".edit-lock");
    if fs::read_to_string(lock.join("owner"))? != reaped_pid.to_string()
        || Path::new(&format!("/proc/{reaped_pid}")).exists()
    {
        return Err(failure("owner not demonstrably dead"));
    }
    if fs::read(root.join("journal"))? != b"PREPARED" {
        return Err(failure("unexpected recovery state"));
    }
    let proposal = fs::read(root.join("staged"))?;
    fs::rename(root.join("staged"), root.join("recovered-proposal"))?;
    fs::write(root.join("journal"), b"RECOVERED_UNAPPLIED")?;
    fs::remove_file(lock.join("owner"))?;
    fs::remove_dir(lock)?;
    Ok(proposal)
}
pub struct Watcher {
    stop: Arc<AtomicBool>,
    worker: Option<JoinHandle<()>>,
    pub hints: Arc<AtomicU64>,
}
impl Watcher {
    pub fn start(path: PathBuf) -> io::Result<Self> {
        let mut last = fs::read(&path)?;
        let stop = Arc::new(AtomicBool::new(false));
        let hints = Arc::new(AtomicU64::new(0));
        let (s, h) = (stop.clone(), hints.clone());
        let worker = thread::spawn(move || {
            while !s.load(Ordering::Acquire) {
                if let Ok(now) = fs::read(&path) {
                    if now != last {
                        last = now;
                        h.fetch_add(1, Ordering::Release);
                    }
                }
                thread::sleep(Duration::from_millis(5));
            }
        });
        Ok(Self {
            stop,
            worker: Some(worker),
            hints,
        })
    }
}
impl Drop for Watcher {
    fn drop(&mut self) {
        self.stop.store(true, Ordering::Release);
        if let Some(w) = self.worker.take() {
            w.join().expect("watcher panicked")
        }
    }
}
pub fn current(path: &Path, snapshot: &[u8]) -> io::Result<bool> {
    Ok(fs::read(path)? == snapshot)
}

pub struct StreamRuntime {
    child: Child,
    workers: Vec<JoinHandle<io::Result<usize>>>,
    pub counts: [Arc<AtomicU64>; 2],
    pub pid: u32,
}
impl StreamRuntime {
    pub fn start(executable: &Path) -> io::Result<Self> {
        let mut child = Command::new(executable)
            .arg("stream")
            .stdin(Stdio::null())
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()?;
        let pid = child.id();
        let counts = [Arc::new(AtomicU64::new(0)), Arc::new(AtomicU64::new(0))];
        fn drain(
            mut reader: impl Read + Send + 'static,
            count: Arc<AtomicU64>,
        ) -> JoinHandle<io::Result<usize>> {
            thread::spawn(move || {
                let mut buffer = [0; 8192];
                let mut kept = Vec::new();
                loop {
                    let n = reader.read(&mut buffer)?;
                    if n == 0 {
                        return Ok(kept.len());
                    }
                    count.fetch_add(n as u64, Ordering::Release);
                    let copy = n.min(4096 - kept.len());
                    kept.extend_from_slice(&buffer[..copy]);
                }
            })
        }
        let workers = vec![
            drain(child.stdout.take().unwrap(), counts[0].clone()),
            drain(child.stderr.take().unwrap(), counts[1].clone()),
        ];
        Ok(Self {
            child,
            workers,
            counts,
            pid,
        })
    }
    pub fn cancel(&mut self) -> io::Result<Vec<usize>> {
        if self.child.try_wait()?.is_none() {
            self.child.kill()?;
        }
        self.child.wait()?;
        self.workers
            .drain(..)
            .map(|w| w.join().map_err(|_| failure("reader panic"))?)
            .collect()
    }
    pub fn joined(&self) -> bool {
        self.workers.is_empty()
    }
}
impl Drop for StreamRuntime {
    fn drop(&mut self) {
        let _ = self.cancel();
    }
}

pub fn publish_allowed(approved: bool, presented: &str, grant: &str) -> bool {
    approved && !grant.is_empty() && presented == grant
}
pub fn serve_once(
    listener: &std::net::TcpListener,
    destination: &Path,
    grant: &str,
) -> io::Result<bool> {
    let (stream, _) = listener.accept()?;
    stream.set_read_timeout(Some(Duration::from_secs(2)))?;
    let mut request = String::new();
    stream.take(1025).read_to_string(&mut request)?;
    if request.len() > 1024 {
        return Err(failure("oversized request"));
    }
    let Some((header, payload)) = request.split_once('\n') else {
        return Err(failure("invalid frame"));
    };
    let (approved, token) = header.split_once(' ').unwrap_or((header, ""));
    if !publish_allowed(approved == "APPROVED", token, grant) {
        return Ok(false);
    }
    let mut f = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(destination)?;
    f.write_all(payload.as_bytes())?;
    Ok(true)
}
