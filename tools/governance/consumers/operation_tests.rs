#![forbid(unsafe_code)]
#[path = "operations.rs"]
mod operations;
use operations::*;
use std::{
    fs,
    path::{Path, PathBuf},
    process::Command,
    sync::atomic::{AtomicUsize, Ordering},
    thread,
    time::{Duration, Instant},
};
static NEXT: AtomicUsize = AtomicUsize::new(0);
fn dir() -> PathBuf {
    let p = std::env::temp_dir().join(format!(
        "ox-op-{}-{}-{}",
        std::process::id(),
        NEXT.fetch_add(1, Ordering::Relaxed),
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    fs::create_dir(&p).unwrap();
    fs::write(p.join("target"), b"base").unwrap();
    p
}
fn fixture() -> PathBuf {
    std::env::var_os("OX_CONSUMER_FIXTURE").unwrap().into()
}
#[test]
fn workspace_ac01_paths() {
    let root = dir();
    let outside = dir();
    std::os::unix::fs::symlink(outside.join("target"), root.join("link")).unwrap();
    assert!(edit(&root, Path::new("../escape"), b"base", b"bad", false).is_err());
    assert!(edit(&root, Path::new("link"), b"base", b"bad", false).is_err());
    assert_eq!(fs::read(outside.join("target")).unwrap(), b"base");
    assert_eq!(fs::read(root.join("target")).unwrap(), b"base");
    assert!(!root.parent().unwrap().join("escape").exists());
    edit(&root, Path::new("target"), b"base", b"good", false).unwrap();
    assert_eq!(fs::read(root.join("target")).unwrap(), b"good");
}
#[test]
fn workspace_ac02_concurrent() {
    let root = dir();
    let mut a = Command::new(fixture())
        .args(["edit", root.to_str().unwrap(), "one"])
        .spawn()
        .unwrap();
    let mut b = Command::new(fixture())
        .args(["edit", root.to_str().unwrap(), "two"])
        .spawn()
        .unwrap();
    let codes = [
        a.wait().unwrap().code().unwrap(),
        b.wait().unwrap().code().unwrap(),
    ];
    assert_eq!(codes.iter().filter(|c| **c == 0).count(), 1);
    assert_eq!(codes.iter().filter(|c| **c == 23).count(), 1);
    assert!(matches!(
        fs::read(root.join("target")).unwrap().as_slice(),
        b"one" | b"two"
    ));
    println!("concurrent exit codes {codes:?}");
}
#[test]
fn workspace_ac03_crash() {
    let root = dir();
    let mut child = Command::new(fixture())
        .args(["edit", root.to_str().unwrap(), "crash"])
        .spawn()
        .unwrap();
    let pid = child.id();
    assert_eq!(child.wait().unwrap().code(), Some(91));
    assert_eq!(fs::read(root.join("target")).unwrap(), b"base");
    assert_eq!(fs::read(root.join("journal")).unwrap(), b"PREPARED");
    assert_eq!(recover_after_reap(&root, pid).unwrap(), b"crash");
    assert_eq!(fs::read(root.join("recovered-proposal")).unwrap(), b"crash");
    assert_eq!(
        fs::read(root.join("journal")).unwrap(),
        b"RECOVERED_UNAPPLIED"
    );
    assert_eq!(fs::read(root.join("target")).unwrap(), b"base");
    assert!(!root.join(".edit-lock").exists());
}
#[test]
fn workspace_ac04_watcher() {
    let root = dir();
    let p = root.join("target");
    let w = Watcher::start(p.clone()).unwrap();
    fs::write(&p, b"external").unwrap();
    let until = Instant::now() + Duration::from_secs(2);
    while w.hints.load(Ordering::Acquire) == 0 && Instant::now() < until {
        thread::sleep(Duration::from_millis(5));
    }
    assert!(w.hints.load(Ordering::Acquire) > 0);
    assert!(!current(&p, b"base").unwrap());
    drop(w);
    fs::write(&p, b"missed-event").unwrap();
    assert!(!current(&p, b"external").unwrap());
    assert!(current(&p, b"missed-event").unwrap());
}
#[test]
fn runtime_ac03_cancel_output() {
    let mut rt = StreamRuntime::start(&fixture()).unwrap();
    let until = Instant::now() + Duration::from_secs(3);
    while rt
        .counts
        .iter()
        .any(|c| c.load(Ordering::Acquire) < 1048576)
        && Instant::now() < until
    {
        thread::sleep(Duration::from_millis(2));
    }
    let before: Vec<_> = rt
        .counts
        .iter()
        .map(|c| c.load(Ordering::Acquire))
        .collect();
    assert!(before.iter().all(|c| *c >= 1048576));
    let start = Instant::now();
    let retained = rt.cancel().unwrap();
    assert!(start.elapsed() < Duration::from_secs(2));
    assert_eq!(retained, vec![4096, 4096]);
    assert!(rt.joined());
    assert!(!Path::new(&format!("/proc/{}", rt.pid)).exists());
    println!(
        "stdout/stderr bytes before cancellation {before:?}; joined=2; retained={retained:?}; elapsed={:?}",
        start.elapsed()
    );
}
#[test]
fn verification_ac04_receiver() {
    use std::io::Write;
    use std::net::{Shutdown, TcpListener, TcpStream};
    assert!(!publish_allowed(true, "", "fixture-grant"));
    assert!(!publish_allowed(false, "fixture-grant", "fixture-grant"));
    assert!(publish_allowed(true, "fixture-grant", "fixture-grant"));
    let root = dir();
    let dest = root.join("published");
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let address = listener.local_addr().unwrap();
    for (token, expected) in [("", false), ("wrong", false), ("fixture-grant", true)] {
        thread::scope(|scope| {
            let server = scope.spawn(|| serve_once(&listener, &dest, "fixture-grant").unwrap());
            let mut c = TcpStream::connect(address).unwrap();
            c.write_all(format!("APPROVED {token}\nartifact").as_bytes())
                .unwrap();
            c.shutdown(Shutdown::Write).unwrap();
            assert_eq!(server.join().unwrap(), expected);
        });
        assert_eq!(dest.exists(), expected);
    }
    assert_eq!(fs::read(dest).unwrap(), b"artifact");
}
#[test]
fn plugin_ac02_no_mutation() {
    let root = dir();
    let binary = PathBuf::from(std::env::var_os("OX_PLUGIN_FIXTURE").unwrap());
    let snapshot = fs::read(root.join("target")).unwrap();
    let before: Vec<_> = fs::read_dir(&root)
        .unwrap()
        .map(|x| x.unwrap().file_name())
        .collect();
    let status = Command::new(fixture())
        .arg("plugin-check")
        .arg(binary)
        .current_dir(&root)
        .status()
        .unwrap();
    assert!(status.success());
    assert_eq!(fs::read(root.join("target")).unwrap(), snapshot);
    let after: Vec<_> = fs::read_dir(&root)
        .unwrap()
        .map(|x| x.unwrap().file_name())
        .collect();
    assert_eq!(before, after);
}
