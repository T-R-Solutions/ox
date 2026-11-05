use ox_ui::local_task::Controller;
use std::{
    fs,
    path::PathBuf,
    sync::{
        Arc,
        atomic::{AtomicBool, Ordering},
    },
    time::{Duration, SystemTime, UNIX_EPOCH},
};
fn setup() -> (Controller, PathBuf) {
    let bins = std::env::current_exe()
        .unwrap()
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .to_owned();
    assert!(
        bins.join("local-task").exists(),
        "cargo build --workspace first"
    );
    let dir = std::env::temp_dir().join(format!(
        "ox-ui-test-{}-{}",
        std::process::id(),
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    fs::create_dir(&dir).unwrap();
    (Controller::new(bins), dir)
}
#[test]
fn real_result_identity_history_invalidation_and_preservation() {
    let (mut c, dir) = setup();
    fs::write(dir.join("user.txt"), b"untouched\0").unwrap();
    assert!(c.select(&dir.join("missing")).is_err());
    assert_eq!(c.attempt, 0);
    c.select(&dir).unwrap();
    assert!(c.verify(true).is_err());
    let cancel = Arc::new(AtomicBool::new(false));
    assert!(
        c.execute("good", cancel.clone())
            .unwrap()
            .contains("Success")
    );
    assert!(c.verify(false).unwrap().contains("UNVERIFIED"));
    assert!(c.verify(true).unwrap().starts_with("APPROVED"));
    let task = fs::read_dir(&dir)
        .unwrap()
        .map(|p| p.unwrap().path())
        .find(|p| p.is_dir())
        .unwrap();
    fs::write(task.join("result.txt"), b"wrong").unwrap();
    let stale = c.verify(false).unwrap();
    assert!(stale.starts_with("UNVERIFIED"));
    assert!(stale.contains("run 1"));
    assert!(c.verify(true).unwrap().starts_with("REJECTED"));
    fs::remove_file(task.join("result.txt")).unwrap();
    assert!(
        c.verify(true)
            .unwrap_err()
            .to_string()
            .contains("No approval is possible")
    );
    assert!(c.verify(false).unwrap().starts_with("UNVERIFIED"));
    assert!(
        c.execute("bad", cancel.clone())
            .unwrap()
            .contains("Success")
    );
    assert!(c.verify(true).unwrap().starts_with("REJECTED"));
    assert!(c.execute("failure", cancel).unwrap().contains("Failed"));
    assert_eq!(fs::read(dir.join("user.txt")).unwrap(), b"untouched\0");
}
#[test]
fn cancellation_and_timeout_observe_exit() {
    let (mut c, dir) = setup();
    c.select(&dir).unwrap();
    let cancel = Arc::new(AtomicBool::new(false));
    let flag = cancel.clone();
    let worker = std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(50));
        flag.store(true, Ordering::Relaxed);
    });
    assert!(c.execute("hang", cancel).unwrap().contains("Cancelled"));
    worker.join().unwrap();
    assert!(
        c.execute("hang", Arc::new(AtomicBool::new(false)))
            .unwrap()
            .contains("TimedOut")
    );
}

#[test]
fn inaccessible_workspace_is_rejected_before_attempt() {
    use std::os::unix::fs::PermissionsExt;
    let (mut c, dir) = setup();
    fs::set_permissions(&dir, fs::Permissions::from_mode(0o000)).unwrap();
    let result = c.select(&dir);
    fs::set_permissions(&dir, fs::Permissions::from_mode(0o700)).unwrap();
    assert!(result.is_err());
    assert_eq!(c.attempt, 0);
}
