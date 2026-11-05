//! In-memory content-bound local verification. Execution is explicitly caller-authorized.
use crate::verdict::Verdict;
use std::{
    fs::File,
    io::{self, Read},
    path::PathBuf,
    process::{Command, Stdio},
    thread,
    time::{Duration, Instant},
};
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
        File::open(&path)?
            .take(16 * 1024 * 1024 + 1)
            .read_to_end(&mut bytes)?;
        total += bytes.len();
        if bytes.len() > 16 * 1024 * 1024 || total > 32 * 1024 * 1024 {
            return Err(invalid("snapshot limit exceeded"));
        }
        content.push(Content { path, bytes });
    }
    Ok(content)
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
    // Regression adapter only: the pre-fix implementation has no cancellation API.
    pub fn execute_cancellable(&mut self, check: &Check, deadline: Duration, _cancel: &std::sync::atomic::AtomicBool) -> io::Result<u64> {
        self.execute(check, deadline)
    }
    pub fn execute(&mut self, check: &Check, deadline: Duration) -> io::Result<u64> {
        if self.observations.len() >= 32 || deadline.is_zero() || deadline > Duration::from_secs(10)
        {
            return Err(invalid("execution limit"));
        }
        let before = capture(check)?;
        let mut child = Command::new(&check.executable)
            .args(&check.arguments)
            .current_dir(&check.directory)
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()?;
        let until = Instant::now() + deadline;
        let result = loop {
            match child.try_wait() {
                Ok(Some(status)) => break ResultKind::Exited(status.code()),
                Err(error) => {
                    let _ = child.kill();
                    let _ = child.wait();
                    return Err(error);
                }
                Ok(None) => {}
            }
            if Instant::now() >= until {
                let _ = child.kill();
                child.wait()?;
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
                reason: "Incomplete or timed-out current observation requires investigation".into(),
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
