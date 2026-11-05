#![forbid(unsafe_code)]
use ox_verification::{
    engine::{Check, Engine, ResultKind},
    verdict::Verdict,
};
use std::{
    path::PathBuf,
    sync::atomic::{AtomicU64, Ordering},
    time::Duration,
};
static NEXT: AtomicU64 = AtomicU64::new(1);
struct Fixture {
    dir: PathBuf,
    check: Check,
}
impl Fixture {
    fn new() -> Self {
        let dir = std::env::temp_dir().join(format!(
            "ox-verify-{}-{}",
            std::process::id(),
            NEXT.fetch_add(1, Ordering::Relaxed)
        ));
        std::fs::create_dir(&dir).unwrap();
        let candidate = dir.join("candidate");
        std::fs::write(&candidate, b"accepted\n").unwrap();
        let check = Check {
            id: "AC-local".into(),
            description: "Literal accepted candidate".into(),
            executable: env!("CARGO_BIN_EXE_local-oracle").into(),
            arguments: vec![candidate.to_str().unwrap().into()],
            directory: dir.clone(),
            inputs: vec![candidate],
            expected_exit: 0,
        };
        Self { dir, check }
    }
    fn write(&self, bytes: &[u8]) {
        std::fs::write(&self.check.inputs[0], bytes).unwrap();
    }
}
impl Drop for Fixture {
    fn drop(&mut self) {
        std::fs::remove_file(self.dir.join("candidate")).unwrap();
        std::fs::remove_dir(&self.dir).unwrap();
    }
}
#[test]
fn approval_requires_observation_not_completion_claims() {
    let f = Fixture::new();
    let mut e = Engine::default();
    e.note_completion("Agent says done; task checkbox complete".into())
        .unwrap();
    assert_eq!(e.evaluate(&f.check), Verdict::NotVerified);
    let run = e.execute(&f.check, Duration::from_secs(1)).unwrap();
    assert_eq!(
        e.evaluate(&f.check),
        Verdict::Approved {
            evidence: format!("run:{run}")
        }
    );
    assert_eq!(e.observations()[0].result(), ResultKind::Exited(Some(0)));
    assert_eq!(e.observations()[0].check(), &f.check);
    assert!(!e.observations()[0].inputs().is_empty());
}
#[test]
fn failure_history_survives_repair_and_content_invalidation_is_selective() {
    let f = Fixture::new();
    let mut other = Fixture::new();
    other.check.id = "AC-independent".into();
    let mut e = Engine::default();
    f.write(b"defect\n");
    let failed = e.execute(&f.check, Duration::from_secs(1)).unwrap();
    assert_eq!(
        e.evaluate(&f.check),
        Verdict::Rejected {
            evidence: format!("run:{failed}")
        }
    );
    e.execute(&other.check, Duration::from_secs(1)).unwrap();
    f.write(b"accepted\n");
    assert_eq!(e.evaluate(&f.check), Verdict::NotVerified);
    assert!(matches!(e.evaluate(&other.check), Verdict::Approved { .. }));
    e.execute(&f.check, Duration::from_secs(1)).unwrap();
    assert!(matches!(e.evaluate(&f.check), Verdict::Approved { .. }));
    assert_eq!(e.observations()[0].result(), ResultKind::Exited(Some(17)));
    assert!(
        e.observations()[0]
            .inputs()
            .iter()
            .any(|x| x.bytes == b"defect\n")
    );
    let mut altered = f.check.clone();
    altered.expected_exit = 17;
    assert_eq!(e.evaluate(&altered), Verdict::NotVerified);
    altered = f.check.clone();
    altered.description.push_str(" changed");
    assert_eq!(e.evaluate(&altered), Verdict::NotVerified);
    f.write(b"changed again");
    assert_eq!(e.evaluate(&f.check), Verdict::NotVerified);
}
#[test]
fn incomplete_and_not_applicable_are_not_approval() {
    let mut f = Fixture::new();
    let mut e = Engine::default();
    f.check.arguments = vec!["hang".into()];
    e.execute(&f.check, Duration::from_millis(30)).unwrap();
    assert!(matches!(e.evaluate(&f.check), Verdict::Inconclusive { .. }));
    assert!(Engine::not_applicable(" ").is_err());
    assert!(matches!(
        Engine::not_applicable("Outside this criterion's platform scope").unwrap(),
        Verdict::NotApplicable { .. }
    ));
}

#[test]
fn contradictory_current_pass_does_not_erase_observed_failure() {
    let mut f = Fixture::new();
    let marker = f.dir.join("external-state");
    f.check.arguments = vec!["flip".into(), marker.to_str().unwrap().into()];
    let mut engine = Engine::default();
    // The fixture deliberately varies an undeclared dependency. Both observations
    // share the declared snapshot: the engine must expose rejection, not last-wins.
    engine.execute(&f.check, Duration::from_secs(1)).unwrap();
    engine.execute(&f.check, Duration::from_secs(1)).unwrap();
    assert_eq!(
        engine.observations()[0].result(),
        ResultKind::Exited(Some(17))
    );
    assert_eq!(
        engine.observations()[1].result(),
        ResultKind::Exited(Some(0))
    );
    assert!(matches!(
        engine.evaluate(&f.check),
        Verdict::Rejected { .. }
    ));
    std::fs::remove_file(marker).unwrap();
}
