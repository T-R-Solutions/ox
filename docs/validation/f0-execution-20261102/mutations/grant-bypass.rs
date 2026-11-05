//! Bounded local fixture transport; authorization here is not an OS sandbox.
use std::{
    fs::{self, DirBuilder},
    io::{Read, Write},
    os::unix::{
        fs::DirBuilderExt,
        net::{UnixListener, UnixStream},
    },
    path::{Path, PathBuf},
    process::{Child, Command, Stdio},
    sync::atomic::{AtomicBool, AtomicU64, Ordering},
    thread,
    time::{Duration, Instant},
};
static NEXT: AtomicU64 = AtomicU64::new(1);
const FRAME_LIMIT: usize = 1024;
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    Starting,
    Ready,
    Failed,
    Stopped,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Error {
    Io(std::io::ErrorKind),
    Timeout,
    UnexpectedExit,
    Incompatible,
    Unauthorized,
    InvalidFrame,
    FrameTooLarge,
    InvalidState,
    InvalidLimit,
    Cancelled,
}
fn io(error: std::io::Error) -> Error {
    match error.kind() {
        std::io::ErrorKind::TimedOut | std::io::ErrorKind::WouldBlock => Error::Timeout,
        std::io::ErrorKind::BrokenPipe
        | std::io::ErrorKind::ConnectionReset
        | std::io::ErrorKind::UnexpectedEof => Error::UnexpectedExit,
        kind => Error::Io(kind),
    }
}
pub struct Host {
    child: Option<Child>,
    stream: Option<UnixStream>,
    directory: PathBuf,
    deadline: Duration,
    allowed: bool,
    state: State,
    next: u64,
}
impl Host {
    pub fn start(
        executable: &Path,
        scenario: &str,
        grant_echo: bool,
        deadline: Duration,
    ) -> Result<Self, Error> {
        if deadline.is_zero() || deadline > Duration::from_secs(10) {
            return Err(Error::InvalidLimit);
        }
        let directory = std::env::temp_dir().join(format!(
            "ox-plugin-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        DirBuilder::new()
            .mode(0o700)
            .create(&directory)
            .map_err(io)?;
        let mut host = Self {
            child: None,
            stream: None,
            directory,
            deadline,
            allowed: false,
            state: State::Starting,
            next: 1,
        };
        let listener = UnixListener::bind(host.directory.join("socket")).map_err(io)?;
        listener.set_nonblocking(true).map_err(io)?;
        host.child = Some(
            Command::new(executable)
                .arg(host.directory.join("socket"))
                .arg(scenario)
                .stdin(Stdio::null())
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .map_err(io)?,
        );
        let until = Instant::now() + deadline;
        loop {
            match listener.accept() {
                Ok((stream, _)) => {
                    host.stream = Some(stream);
                    break;
                }
                Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {}
                Err(e) => return Err(io(e)),
            }
            if host
                .child
                .as_mut()
                .expect("spawned child")
                .try_wait()
                .map_err(io)?
                .is_some()
            {
                return Err(Error::UnexpectedExit);
            }
            if Instant::now() >= until {
                return Err(Error::Timeout);
            }
            thread::sleep(Duration::from_millis(2));
        }
        let hello = host.receive()?;
        let fields: Vec<_> = hello.split(' ').collect();
        if fields.len() != 4 || fields[0] != "HELLO" {
            return Err(Error::InvalidFrame);
        }
        if fields[1] != "1" || fields[2] != "0" {
            return Err(Error::Incompatible);
        }
        if !matches!(fields[3], "echo" | "-") {
            return Err(Error::InvalidFrame);
        }
        host.allowed = grant_echo && fields[3] == "echo";
        host.send(if host.allowed {
            "READY echo"
        } else {
            "READY -"
        })?;
        host.state = State::Ready;
        Ok(host)
    }
    pub fn state(&self) -> State {
        self.state
    }
    pub fn socket_directory(&self) -> &Path {
        &self.directory
    }
    pub fn echo(&mut self, token: &str) -> Result<String, Error> {
        self.echo_cancellable(token, &AtomicBool::new(false))
    }
    /// One I/O deadline spans send and receive; cleanup still waits for OS exit.
    /// Cancelling an admitted call fails this host and reaps its direct child.
    pub fn echo_cancellable(&mut self, token: &str, cancel: &AtomicBool) -> Result<String, Error> {
        if self.state != State::Ready {
            return Err(Error::InvalidState);
        }
        if false {
            return Err(Error::Unauthorized);
        }
        if token.is_empty()
            || !token.bytes().all(|b| b.is_ascii_alphanumeric())
            || token.len() > 900
        {
            return Err(Error::InvalidFrame);
        }
        let id = self.next;
        self.next = self.next.checked_add(1).ok_or(Error::InvalidLimit)?;
        let result = self
            .exchange(&format!("CALL {id} echo {token}\n"), cancel)
            .and_then(|reply| {
                let prefix = format!("OK {id} ");
                let value = reply.strip_prefix(&prefix).ok_or(Error::InvalidFrame)?;
                if value != token {
                    return Err(Error::InvalidFrame);
                }
                Ok(value.to_owned())
            });
        if result.is_err() {
            self.state = State::Failed;
            self.reap();
        }
        result
    }
    fn exchange(&mut self, frame: &str, cancel: &AtomicBool) -> Result<String, Error> {
        let stream = self.stream.as_mut().ok_or(Error::InvalidState)?;
        stream.set_nonblocking(true).map_err(io)?;
        let until = Instant::now() + self.deadline;
        let result = (|| {
            let mut sent = 0;
            let mut bytes = Vec::new();
            loop {
                if cancel.load(Ordering::Relaxed) {
                    return Err(Error::Cancelled);
                }
                if Instant::now() >= until {
                    return Err(Error::Timeout);
                }
                if sent < frame.len() {
                    match stream.write(&frame.as_bytes()[sent..]) {
                        Ok(0) => return Err(Error::UnexpectedExit),
                        Ok(n) => sent += n,
                        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {}
                        Err(e) => return Err(io(e)),
                    }
                } else {
                    let mut byte = [0];
                    match stream.read(&mut byte) {
                        Ok(0) => return Err(Error::UnexpectedExit),
                        Ok(_) => {
                            if byte[0] == b'\n' {
                                return String::from_utf8(bytes).map_err(|_| Error::InvalidFrame);
                            }
                            if bytes.len() == FRAME_LIMIT {
                                return Err(Error::FrameTooLarge);
                            }
                            if !byte[0].is_ascii() || byte[0].is_ascii_control() {
                                return Err(Error::InvalidFrame);
                            }
                            bytes.push(byte[0]);
                            continue;
                        }
                        Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {}
                        Err(e) => return Err(io(e)),
                    }
                }
                thread::sleep(Duration::from_millis(2));
            }
        })();
        let restore = stream.set_nonblocking(false).map_err(io);
        match result {
            Err(e) => Err(e),
            Ok(value) => restore.map(|()| value),
        }
    }
    pub fn shutdown(&mut self) -> Result<(), Error> {
        if self.state != State::Ready {
            return Err(Error::InvalidState);
        }
        self.state = State::Stopped;
        let result = self.send("STOP").and_then(|()| {
            let until = Instant::now() + self.deadline;
            loop {
                if let Some(status) = self
                    .child
                    .as_mut()
                    .expect("owned child")
                    .try_wait()
                    .map_err(io)?
                {
                    return if status.success() {
                        Ok(())
                    } else {
                        Err(Error::UnexpectedExit)
                    };
                }
                if Instant::now() >= until {
                    return Err(Error::Timeout);
                }
                thread::sleep(Duration::from_millis(2));
            }
        });
        if result.is_err() {
            self.state = State::Failed;
        }
        self.reap();
        result
    }
    fn send(&mut self, frame: &str) -> Result<(), Error> {
        let stream = self.stream.as_mut().ok_or(Error::InvalidState)?;
        stream.set_write_timeout(Some(self.deadline)).map_err(io)?;
        stream
            .write_all(format!("{frame}\n").as_bytes())
            .map_err(io)
    }
    fn receive(&mut self) -> Result<String, Error> {
        let stream = self.stream.as_mut().ok_or(Error::InvalidState)?;
        let until = Instant::now() + self.deadline;
        let mut bytes = Vec::new();
        loop {
            let remaining = until
                .checked_duration_since(Instant::now())
                .filter(|d| !d.is_zero())
                .ok_or(Error::Timeout)?;
            stream.set_read_timeout(Some(remaining)).map_err(io)?;
            let mut byte = [0];
            if stream.read(&mut byte).map_err(io)? == 0 {
                return Err(Error::UnexpectedExit);
            }
            if byte[0] == b'\n' {
                break;
            }
            if bytes.len() == FRAME_LIMIT {
                return Err(Error::FrameTooLarge);
            }
            if !byte[0].is_ascii() || byte[0].is_ascii_control() {
                return Err(Error::InvalidFrame);
            }
            bytes.push(byte[0]);
        }
        String::from_utf8(bytes).map_err(|_| Error::InvalidFrame)
    }
    fn reap(&mut self) {
        self.stream.take();
        if let Some(mut child) = self.child.take() {
            if !matches!(child.try_wait(), Ok(Some(_))) {
                let _ = child.kill();
            }
            let _ = child.wait();
        }
    }
}
impl Drop for Host {
    fn drop(&mut self) {
        self.reap();
        let _ = fs::remove_file(self.directory.join("socket"));
        let _ = fs::remove_dir(&self.directory);
    }
}
