#![forbid(unsafe_code)]
#![allow(dead_code)]
// Standalone test consumer of the unchanged production modules; no substitute engine.
#[path = "../../../application/crates/ox-agent/src/runtime.rs"]
mod runtime;
#[path = "../../../application/crates/ox-verification/src/verdict.rs"]
mod verdict;
#[path = "../../../application/crates/ox-verification/src/engine.rs"]
mod engine;

#[test]
fn failed_direct_child_is_reaped() {
    use runtime::{Identity, Outcome, Runtime, State};
    use std::{path::Path, time::{Duration, Instant}};
    let exe = std::fs::canonicalize("application/target/debug/local-agent").unwrap();
    let mut child = Runtime::spawn(&exe, "failure", Path::new("/tmp"),
        Identity { session: 1, task: 1, attempt: 1 }, Duration::from_secs(1)).unwrap();
    let pid = child.pid();
    let deadline = Instant::now() + Duration::from_secs(3);
    while child.poll().unwrap() == State::Running {
        assert!(Instant::now() < deadline);
        std::thread::sleep(Duration::from_millis(2));
    }
    assert_eq!(child.state(), State::Finished(Outcome::Failed(Some(17))));
    assert!(!Path::new(&format!("/proc/{pid}")).exists(), "child still present, including zombie");
}

#[test]
fn absent_oracle_cannot_create_approval_or_observation() {
    use engine::{Check, Engine};
    use verdict::Verdict;
    let dir = std::env::temp_dir().join(format!("ox-skill-missing-oracle-{}", std::process::id()));
    std::fs::create_dir(&dir).unwrap();
    let input = dir.join("candidate");
    std::fs::write(&input, b"accepted\n").unwrap();
    let check = Check { id: "AC-02".into(), description: "Absent executable".into(),
        executable: dir.join("does-not-exist"), arguments: vec![], directory: dir.clone(),
        inputs: vec![input.clone()], expected_exit: 0 };
    let mut engine = Engine::default();
    engine.note_completion("done".into()).unwrap();
    assert_eq!(engine.evaluate(&check), Verdict::NotVerified);
    assert_eq!(engine.execute(&check, std::time::Duration::from_secs(1)).unwrap_err().kind(),
        std::io::ErrorKind::NotFound);
    assert!(engine.observations().is_empty());
    assert_eq!(engine.evaluate(&check), Verdict::NotVerified);
    std::fs::remove_file(input).unwrap();
    std::fs::remove_dir(dir).unwrap();
}
