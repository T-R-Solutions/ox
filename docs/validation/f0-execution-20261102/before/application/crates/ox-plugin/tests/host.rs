#![forbid(unsafe_code)]
use ox_plugin::host::{Error, Host, State};
use std::{
    path::Path,
    time::{Duration, Instant},
};
fn start(mode: &str, grant: bool) -> Result<Host, Error> {
    Host::start(
        Path::new(env!("CARGO_BIN_EXE_local-plugin")),
        mode,
        grant,
        Duration::from_millis(300),
    )
}
#[test]
fn real_process_negotiation_shutdown_and_recovery() {
    let mut host = start("echo", true).unwrap();
    let directory = host.socket_directory().to_owned();
    assert_eq!(host.echo("hello42"), Ok("hello42".into()));
    assert_eq!(host.echo("again"), Ok("again".into()));
    host.shutdown().unwrap();
    assert_eq!(host.state(), State::Stopped);
    assert_eq!(host.echo("late"), Err(Error::InvalidState));
    drop(host);
    assert!(!directory.exists());
    let mut recovered = start("echo", true).unwrap();
    assert_ne!(directory, recovered.socket_directory());
    assert_eq!(recovered.echo("new"), Ok("new".into()));
    recovered.shutdown().unwrap();
}
#[test]
fn incompatible_and_unauthorized_are_rejected() {
    assert!(matches!(
        start("incompatible", true),
        Err(Error::Incompatible)
    ));
    for (mode, grant) in [("denied", false), ("unsupported", true)] {
        let mut host = start(mode, grant).unwrap();
        assert_eq!(host.echo("secret"), Err(Error::Unauthorized));
        // Fixture exits 21 if it receives ANY CALL, making this an independent oracle.
        host.shutdown().unwrap();
    }
}
#[test]
fn malformed_oversized_and_wrong_correlation_fail_closed() {
    for (mode, error) in [
        ("malformed", Error::InvalidFrame),
        ("oversized", Error::FrameTooLarge),
        ("mismatch", Error::InvalidFrame),
    ] {
        let mut host = start(mode, true).unwrap();
        assert_eq!(host.echo("data"), Err(error));
        assert_eq!(host.state(), State::Failed);
        assert_eq!(host.echo("late"), Err(Error::InvalidState));
    }
}
#[test]
fn timeout_and_crash_are_distinct_and_bounded() {
    for (mode, error) in [
        ("timeout", Error::Timeout),
        ("crash", Error::UnexpectedExit),
    ] {
        let mut host = start(mode, true).unwrap();
        let begin = Instant::now();
        assert_eq!(host.echo("data"), Err(error));
        assert!(begin.elapsed() < Duration::from_secs(3));
        assert_eq!(host.state(), State::Failed);
    }
}
