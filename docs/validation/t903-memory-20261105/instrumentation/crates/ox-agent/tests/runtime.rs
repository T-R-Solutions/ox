#![forbid(unsafe_code)]
use ox_agent::runtime::{Event, Identity, Kind, Machine, Outcome, Runtime, State};
use std::{
    path::Path,
    thread,
    time::{Duration, Instant},
};
fn identity(attempt: u64) -> Identity {
    Identity {
        session: 7,
        task: 11,
        attempt,
    }
}
fn spawn(mode: &str, attempt: u64, workspace: &Path, ms: u64) -> Runtime {
    Runtime::spawn(
        Path::new(env!("CARGO_BIN_EXE_local-agent")),
        mode,
        workspace,
        identity(attempt),
        Duration::from_millis(ms),
    )
    .unwrap()
}
fn finish(runtime: &mut Runtime) -> State {
    let end = Instant::now() + Duration::from_secs(3);
    loop {
        let state = runtime.poll().unwrap();
        if matches!(state, State::Finished(_)) {
            return state;
        }
        assert!(Instant::now() < end);
        thread::sleep(Duration::from_millis(2));
    }
}
#[test]
fn real_success_and_failure_are_observed() {
    for (mode, outcome) in [
        ("success", Outcome::Success),
        ("failure", Outcome::Failed(Some(17))),
    ] {
        let mut r = spawn(mode, 1, Path::new("/tmp"), 1000);
        assert!(r.pid() > 0);
        assert!(!r.output_available());
        assert_eq!(finish(&mut r), State::Finished(outcome));
        assert_eq!(
            r.events().iter().map(|e| e.sequence).collect::<Vec<_>>(),
            vec![1, 2]
        );
        assert_eq!(r.cancel().unwrap(), State::Finished(outcome));
    }
}
#[test]
fn cancellation_and_deadline_reap_before_recovery() {
    let mut r = spawn("hang", 1, Path::new("/tmp"), 1000);
    assert_eq!(r.cancel().unwrap(), State::Cancelling);
    assert_eq!(finish(&mut r), State::Finished(Outcome::Cancelled));
    assert_eq!(
        r.events().iter().map(|e| e.sequence).collect::<Vec<_>>(),
        vec![1, 2, 3]
    );
    let mut timeout = spawn("hang", 2, Path::new("/tmp"), 30);
    assert_eq!(finish(&mut timeout), State::Finished(Outcome::TimedOut));
    let mut recovered = spawn("success", 3, Path::new("/tmp"), 1000);
    assert_eq!(finish(&mut recovered), State::Finished(Outcome::Success));
    assert_eq!(recovered.events()[0].identity.attempt, 3);
    assert_eq!(r.state(), State::Finished(Outcome::Cancelled));
}
#[test]
fn late_duplicate_and_out_of_order_events_leave_state_intact() {
    let mut m = Machine::new(identity(2));
    let start = Event {
        identity: identity(2),
        sequence: 1,
        kind: Kind::Started,
    };
    assert!(!m.apply(Event {
        identity: identity(1),
        ..start
    }));
    assert!(!m.apply(Event {
        sequence: 2,
        ..start
    }));
    assert!(m.apply(start));
    assert!(!m.apply(start));
    assert!(!m.apply(Event {
        sequence: 3,
        kind: Kind::Exited(Outcome::Success),
        ..start
    }));
    assert!(m.apply(Event {
        sequence: 2,
        kind: Kind::Exited(Outcome::Failed(Some(17))),
        ..start
    }));
    assert!(!m.apply(Event {
        sequence: 3,
        kind: Kind::Exited(Outcome::Success),
        ..start
    }));
    assert_eq!(m.state(), State::Finished(Outcome::Failed(Some(17))));
    assert_eq!(m.events().len(), 2);
}
#[test]
fn controlled_adapter_preserves_workspace() {
    let dir = std::env::temp_dir().join(format!("ox-agent-sentinel-{}", std::process::id()));
    std::fs::create_dir(&dir).unwrap();
    let bytes = b"preexisting user content\0\xff";
    std::fs::write(dir.join("sentinel"), bytes).unwrap();
    let mut r = spawn("success", 1, &dir, 1000);
    finish(&mut r);
    assert_eq!(std::fs::read(dir.join("sentinel")).unwrap(), bytes);
    assert_eq!(std::fs::read_dir(&dir).unwrap().count(), 1);
    std::fs::remove_file(dir.join("sentinel")).unwrap();
    std::fs::remove_dir(dir).unwrap();
}
