//! Local no-output adapter supervision. Direct-child control is not a sandbox.
use std::{
    io,
    path::Path,
    process::{Child, Command, ExitStatus, Stdio},
    time::{Duration, Instant},
};
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Identity {
    pub session: u64,
    pub task: u64,
    pub attempt: u64,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Outcome {
    Success,
    Failed(Option<i32>),
    Cancelled,
    TimedOut,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum State {
    Idle,
    Running,
    Cancelling,
    Finished(Outcome),
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Kind {
    Started,
    CancelRequested,
    Exited(Outcome),
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Event {
    pub identity: Identity,
    pub sequence: u64,
    pub kind: Kind,
}
#[derive(Debug)]
pub struct Machine {
    identity: Identity,
    state: State,
    events: Vec<Event>,
}
impl Machine {
    pub fn new(identity: Identity) -> Self {
        Self {
            identity,
            state: State::Idle,
            events: Vec::new(),
        }
    }
    pub fn state(&self) -> State {
        self.state
    }
    pub fn events(&self) -> &[Event] {
        &self.events
    }
    /// A reducer, not an authentication boundary; Runtime supplies observed events.
    pub fn apply(&mut self, event: Event) -> bool {
        if event.identity != self.identity || event.sequence != self.events.len() as u64 + 1 {
            return false;
        }
        let next = match (self.state, event.kind) {
            (State::Idle, Kind::Started) => State::Running,
            (State::Running, Kind::CancelRequested) => State::Cancelling,
            (State::Running, Kind::Exited(o @ (Outcome::Success | Outcome::Failed(_)))) => {
                State::Finished(o)
            }
            (State::Cancelling, Kind::Exited(o @ (Outcome::Cancelled | Outcome::TimedOut))) => {
                State::Finished(o)
            }
            _ => return false,
        };
        self.state = next;
        self.events.push(event);
        true
    }
    fn emit(&mut self, kind: Kind) {
        assert!(self.apply(Event {
            identity: self.identity,
            sequence: self.events.len() as u64 + 1,
            kind
        }));
    }
}
pub struct Runtime {
    machine: Machine,
    child: Option<Child>,
    expires: Instant,
    cancellation: Option<Outcome>,
    pid: u32,
}
impl Runtime {
    pub fn spawn(
        executable: &Path,
        mode: &str,
        workspace: &Path,
        identity: Identity,
        limit: Duration,
    ) -> io::Result<Self> {
        if !executable.is_absolute() || limit.is_zero() || limit > Duration::from_secs(10) {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "absolute executable and deadline (0,10s] required",
            ));
        }
        let child = Command::new(executable)
            .arg(mode)
            .current_dir(workspace)
            .stdin(Stdio::null())
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()?;
        let pid = child.id();
        let mut machine = Machine::new(identity);
        machine.emit(Kind::Started);
        Ok(Self {
            machine,
            child: Some(child),
            expires: Instant::now() + limit,
            cancellation: None,
            pid,
        })
    }
    pub fn state(&self) -> State {
        self.machine.state()
    }
    pub fn events(&self) -> &[Event] {
        self.machine.events()
    }
    pub fn pid(&self) -> u32 {
        self.pid
    }
    pub fn output_available(&self) -> bool {
        false
    }
    pub fn poll(&mut self) -> io::Result<State> {
        if let Some(child) = self.child.as_mut() {
            if let Some(status) = child.try_wait()? {
                self.finish(status);
            } else if self.cancellation.is_none() && Instant::now() >= self.expires {
                self.request_stop(Outcome::TimedOut)?;
            }
        }
        Ok(self.state())
    }
    pub fn cancel(&mut self) -> io::Result<State> {
        self.poll()?;
        if self.state() == State::Running {
            self.request_stop(Outcome::Cancelled)?;
        }
        Ok(self.state())
    }
    fn request_stop(&mut self, outcome: Outcome) -> io::Result<()> {
        self.machine.emit(Kind::CancelRequested);
        self.cancellation = Some(outcome);
        let child = self.child.as_mut().expect("running child");
        if let Err(error) = child.kill() {
            if let Some(status) = child.try_wait()? {
                self.finish(status);
                return Ok(());
            }
            return Err(error);
        }
        // The OS exit is observed on poll; sending kill alone is not completion.
        Ok(())
    }
    fn finish(&mut self, status: ExitStatus) {
        let outcome = self.cancellation.unwrap_or_else(|| {
            if status.success() {
                Outcome::Success
            } else {
                Outcome::Failed(status.code())
            }
        });
        self.machine.emit(Kind::Exited(outcome));
        self.child.take();
    }
}
impl Drop for Runtime {
    fn drop(&mut self) {
        if let Some(mut child) = self.child.take() {
            if !matches!(child.try_wait(), Ok(Some(_))) {
                let _ = child.kill();
            }
            let _ = child.wait();
        }
    }
}
