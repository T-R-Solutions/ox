//! Initialization failure is observed in a bounded child, without mutating process globals.
#![forbid(unsafe_code)]
use std::{
    process::{Command, Stdio},
    thread,
    time::{Duration, Instant},
};
#[test]
fn missing_display_fails_instead_of_reporting_success() {
    let mut child = Command::new(env!("CARGO_BIN_EXE_ox"))
        .env_remove("WAYLAND_DISPLAY")
        .env("DISPLAY", "invalid-display")
        .env("XDG_RUNTIME_DIR", "/nonexistent-ox-test-runtime")
        .stdout(Stdio::null())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    let deadline = Instant::now() + Duration::from_secs(10);
    loop {
        if let Some(status) = child.try_wait().unwrap() {
            let output = child.wait_with_output().unwrap();
            assert!(!status.success());
            assert!(
                !output.stderr.is_empty(),
                "initialization failure needs a diagnostic"
            );
            break;
        }
        if Instant::now() >= deadline {
            let _ = child.kill();
            let _ = child.wait();
            panic!("initialization did not fail within 10s");
        }
        thread::sleep(Duration::from_millis(20));
    }
}
