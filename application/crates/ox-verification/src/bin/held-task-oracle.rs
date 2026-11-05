//! Test-only held oracle for graphical cancellation/close observations.
#![forbid(unsafe_code)]
fn main() {
    std::fs::write("oracle-ready", std::process::id().to_string()).unwrap();
    std::thread::sleep(std::time::Duration::from_secs(30));
}
