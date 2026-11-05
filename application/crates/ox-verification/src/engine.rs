//! In-memory content-bound local verification. Execution is explicitly caller-authorized.
use crate::verdict::Verdict;
use std::{
    fs::{File, OpenOptions},
    io::{self, Read},
    path::PathBuf,
    process::{Child, Command, ExitStatus, Stdio},
    sync::atomic::{AtomicBool, Ordering},
    thread,
    time::{Duration, Instant},
};
const CAPTURE_LIMIT: usize = 32 * 1024 * 1024;
const HISTORY_LIMIT: usize = 128 * 1024 * 1024;
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Check {
    pub id: String,
    pub description: String,
    pub executable: PathBuf,
    pub arguments: Vec<String>,
    pub directory: PathBuf,
    pub inputs: Vec<PathBuf>,
    pub expected_exit: i32,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Content {
    pub path: PathBuf,
    pub bytes: Vec<u8>,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ResultKind {
    Exited(Option<i32>),
    TimedOut,
    Cancelled,
}
#[derive(Debug, Clone)]
pub struct Observation {
    run: u64,
    check: Check,
    before: Vec<Content>,
    after: Vec<Content>,
    result: ResultKind,
}
impl Observation {
    pub fn run(&self) -> u64 {
        self.run
    }
    pub fn check(&self) -> &Check {
        &self.check
    }
    pub fn inputs(&self) -> &[Content] {
        &self.before
    }
    pub fn result(&self) -> ResultKind {
        self.result
    }
}
#[derive(Default)]
pub struct Engine {
    observations: Vec<Observation>,
    claims: Vec<String>,
}
fn invalid(message: &str) -> io::Error {
    io::Error::new(io::ErrorKind::InvalidInput, message)
}
fn capture(check: &Check) -> io::Result<Vec<Content>> {
    if check.id.is_empty()
        || check.description.is_empty()
        || check.inputs.is_empty()
        || check.inputs.len() > 8
        || !check.directory.is_absolute()
    {
        return Err(invalid(
            "explicit criterion, directory and 1..8 inputs required",
        ));
    }
    let mut paths = check.inputs.clone();
    paths.push(check.executable.clone());
    if paths.iter().any(|p| !p.is_absolute()) {
        return Err(invalid("absolute inputs required"));
    }
    paths.sort();
    paths.dedup();
    let mut content = Vec::new();
    let mut total = 0;
    for path in paths {
        let mut bytes = Vec::new();
        regular_file(&path)?
            .take(16 * 1024 * 1024 + 1)
            .read_to_end(&mut bytes)?;
        total += bytes.len();
        if bytes.len() > 16 * 1024 * 1024 || total > CAPTURE_LIMIT {
            return Err(invalid("snapshot limit exceeded"));
        }
        content.push(Content { path, bytes });
    }
    Ok(content)
}
// Metadata is an admission check, not an atomic snapshot or a filesystem deadline.
fn regular_file(path: &std::path::Path) -> io::Result<File> {
    if !std::fs::metadata(path)?.is_file() {
        return Err(invalid("evidence must be a regular file"));
    }
    let mut options = OpenOptions::new();
    options.read(true);
    #[cfg(target_os = "linux")]
    {
        use std::os::unix::fs::OpenOptionsExt;
        // Linux UAPI O_NONBLOCK (asm-generic/fcntl.h). Covers replacement by
        // a FIFO before open; does not bound regular-file or metadata I/O.
        options.custom_flags(0o4000);
    }
    let file = options.open(path)?;
    if !file.metadata()?.is_file() {
        return Err(invalid("opened evidence is not a regular file"));
    }
    Ok(file)
}

trait ChildOps {
    fn poll(&mut self) -> io::Result<Option<ExitStatus>>;
    fn terminate(&mut self) -> io::Result<()>;
    fn reap(&mut self) -> io::Result<ExitStatus>;
}
impl ChildOps for Child {
    fn poll(&mut self) -> io::Result<Option<ExitStatus>> {
        self.try_wait()
    }
    fn terminate(&mut self) -> io::Result<()> {
        self.kill()
    }
    fn reap(&mut self) -> io::Result<ExitStatus> {
        self.wait()
    }
}
#[derive(Debug)]
struct CleanupFailure {
    original: io::Error,
    cleanup: io::Error,
}
impl std::fmt::Display for CleanupFailure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}; {}", self.original, self.cleanup)
    }
}
impl std::error::Error for CleanupFailure {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        Some(&self.original)
    }
}
struct OwnedChild<C: ChildOps> {
    child: C,
    reaped: bool,
}
impl<C: ChildOps> OwnedChild<C> {
    // Always attempt wait even when poll/kill fails. Reap can block; no universal
    // shutdown deadline or descendant ownership is claimed. Errors remain visible.
    fn cleanup(&mut self) -> io::Result<()> {
        if self.reaped {
            return Ok(());
        }
        let mut errors = Vec::new();
        match self.child.poll() {
            Ok(Some(_)) => {
                self.reaped = true;
                return Ok(());
            }
            Ok(None) => {}
            Err(e) => errors.push(format!("cleanup try_wait: {e}")),
        }
        if let Err(e) = self.child.terminate() {
            errors.push(format!("cleanup kill: {e}"));
        }
        match self.child.reap() {
            Ok(_) => self.reaped = true,
            Err(e) => errors.push(format!("cleanup wait: {e}")),
        }
        if errors.is_empty() {
            Ok(())
        } else {
            Err(io::Error::other(errors.join("; ")))
        }
    }
    fn with_cleanup(&mut self, original: io::Error) -> io::Error {
        match self.cleanup() {
            Ok(()) => original,
            Err(cleanup) => io::Error::new(original.kind(), CleanupFailure { original, cleanup }),
        }
    }
}
impl<C: ChildOps> Drop for OwnedChild<C> {
    fn drop(&mut self) {
        if let Err(error) = self.cleanup() {
            eprintln!("verification child cleanup failed (termination/reap unconfirmed): {error}");
        }
    }
}
impl Engine {
    pub fn observations(&self) -> &[Observation] {
        &self.observations
    }
    pub fn note_completion(&mut self, note: String) -> io::Result<()> {
        if self.claims.len() >= 32 || note.len() > 1024 {
            return Err(invalid("claim limit"));
        }
        self.claims.push(note);
        Ok(())
    }
    pub fn execute(&mut self, check: &Check, deadline: Duration) -> io::Result<u64> {
        self.execute_cancellable(check, deadline, &AtomicBool::new(false))
    }
    /// The deadline bounds subprocess supervision, not filesystem capture or OS reap.
    /// Cancellation is terminal only after the owned direct child has been reaped.
    pub fn execute_cancellable(
        &mut self,
        check: &Check,
        deadline: Duration,
        cancel: &AtomicBool,
    ) -> io::Result<u64> {
        if self.observations.len() >= 32 || deadline.is_zero() || deadline > Duration::from_secs(10)
        {
            return Err(invalid("execution limit"));
        }
        let before = capture(check)?;
        let retained: usize = self
            .observations
            .iter()
            .flat_map(|o| o.before.iter().chain(&o.after))
            .map(|input| input.bytes.len())
            .sum();
        let before_size: usize = before.iter().map(|input| input.bytes.len()).sum();
        // Reserve the maximum post-capture before allowing the external effect.
        // Inputs may change while the oracle runs; never evict prior evidence.
        if retained + before_size + CAPTURE_LIMIT > HISTORY_LIMIT {
            return Err(invalid(
                "history content budget (128 MiB) exhausted; no oracle launched; previous observations retained",
            ));
        }
        if cancel.load(Ordering::Relaxed) {
            return Err(io::Error::new(
                io::ErrorKind::Interrupted,
                "verification cancelled before launch",
            ));
        }
        let child = Command::new(&check.executable)
            .args(&check.arguments)
            .current_dir(&check.directory)
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()?;
        let mut child = OwnedChild {
            child,
            reaped: false,
        };
        let until = Instant::now() + deadline;
        let result = loop {
            if cancel.load(Ordering::Relaxed) {
                child.cleanup().map_err(|error| child.with_cleanup(error))?;
                break ResultKind::Cancelled;
            }
            match child.child.try_wait() {
                Ok(Some(status)) => {
                    child.reaped = true;
                    break ResultKind::Exited(status.code());
                }
                Err(error) => {
                    return Err(child.with_cleanup(error));
                }
                Ok(None) => {}
            }
            if Instant::now() >= until {
                child.cleanup().map_err(|error| child.with_cleanup(error))?;
                break ResultKind::TimedOut;
            }
            thread::sleep(Duration::from_millis(2));
        };
        // Missing or unreadable post-inputs cannot produce adequate evidence.
        let after = capture(check).unwrap_or_default();
        let run = self.observations.len() as u64 + 1;
        self.observations.push(Observation {
            run,
            check: check.clone(),
            before,
            after,
            result,
        });
        Ok(run)
    }
    pub fn evaluate(&self, check: &Check) -> Verdict {
        let Ok(current) = capture(check) else {
            return Verdict::NotVerified;
        };
        let mut pass = None;
        let mut incomplete = false;
        for observation in &self.observations {
            if observation.check != *check || observation.before != current {
                continue;
            }
            if observation.before != observation.after {
                incomplete = true;
                continue;
            }
            match observation.result {
                ResultKind::Exited(Some(code)) if code == check.expected_exit => {
                    pass = Some(observation.run)
                }
                ResultKind::Exited(_) => {
                    return Verdict::Rejected {
                        evidence: format!("run:{}", observation.run),
                    };
                }
                ResultKind::TimedOut | ResultKind::Cancelled => incomplete = true,
            }
        }
        if incomplete {
            return Verdict::Inconclusive {
                reason:
                    "Incomplete, cancelled or timed-out current observation requires investigation"
                        .into(),
            };
        }
        match pass {
            Some(run) => Verdict::Approved {
                evidence: format!("run:{run}"),
            },
            None => Verdict::NotVerified,
        }
    }
    pub fn not_applicable(reason: &str) -> io::Result<Verdict> {
        if reason.trim().is_empty() {
            return Err(invalid("nonempty applicability rationale required"));
        }
        Ok(Verdict::NotApplicable {
            reason: reason.to_owned(),
        })
    }
}

#[cfg(test)]
mod ownership_tests {
    use super::*;
    use std::{collections::VecDeque, os::unix::process::ExitStatusExt};
    struct Fake {
        polls: VecDeque<io::Result<Option<ExitStatus>>>,
        kills: VecDeque<io::Result<()>>,
        waits: VecDeque<io::Result<ExitStatus>>,
        calls: Vec<&'static str>,
    }
    impl ChildOps for Fake {
        fn poll(&mut self) -> io::Result<Option<ExitStatus>> {
            self.calls.push("poll");
            self.polls.pop_front().unwrap_or(Ok(None))
        }
        fn terminate(&mut self) -> io::Result<()> {
            self.calls.push("kill");
            self.kills.pop_front().unwrap_or(Ok(()))
        }
        fn reap(&mut self) -> io::Result<ExitStatus> {
            self.calls.push("wait");
            self.waits
                .pop_front()
                .unwrap_or(Ok(ExitStatus::from_raw(0)))
        }
    }
    fn owner() -> OwnedChild<Fake> {
        OwnedChild {
            child: Fake {
                polls: VecDeque::new(),
                kills: VecDeque::new(),
                waits: VecDeque::new(),
                calls: Vec::new(),
            },
            reaped: false,
        }
    }
    #[test]
    fn injected_poll_kill_wait_failures_preserve_original_and_retry_ownership() {
        let mut owner = owner();
        owner
            .child
            .polls
            .push_back(Err(io::Error::other("poll fault")));
        owner
            .child
            .kills
            .push_back(Err(io::Error::other("kill fault")));
        owner
            .child
            .waits
            .push_back(Err(io::Error::other("wait fault")));
        let error = owner.with_cleanup(io::Error::new(io::ErrorKind::PermissionDenied, "original"));
        assert_eq!(error.kind(), io::ErrorKind::PermissionDenied);
        let detail = error
            .get_ref()
            .unwrap()
            .downcast_ref::<CleanupFailure>()
            .unwrap();
        assert_eq!(detail.original.to_string(), "original");
        for text in ["original", "poll fault", "kill fault", "wait fault"] {
            assert!(error.to_string().contains(text));
        }
        assert_eq!(owner.child.calls, ["poll", "kill", "wait"]);
        assert!(!owner.reaped);
        owner.cleanup().unwrap();
        assert!(owner.reaped);
        assert_eq!(
            owner.child.calls,
            ["poll", "kill", "wait", "poll", "kill", "wait"]
        );
    }
    #[test]
    fn injected_kill_failure_still_waits_and_observed_exit_needs_no_kill() {
        let mut owner = owner();
        owner
            .child
            .kills
            .push_back(Err(io::Error::other("kill fault")));
        assert!(owner.cleanup().is_err());
        assert!(owner.reaped);
        assert_eq!(owner.child.calls, ["poll", "kill", "wait"]);
        owner.cleanup().unwrap();
        assert_eq!(owner.child.calls.len(), 3);
        let mut exited = super::ownership_tests::owner();
        exited
            .child
            .polls
            .push_back(Ok(Some(ExitStatus::from_raw(0))));
        exited.cleanup().unwrap();
        assert!(exited.reaped);
        assert_eq!(exited.child.calls, ["poll"]);
    }
}
