//! Controlled no-output process; does not read/write the workspace or use a provider.
#![forbid(unsafe_code)]
fn main() {
    match std::env::args().nth(1).as_deref() {
        Some("success") => {}
        Some("failure") => std::process::exit(17),
        Some("hang") => std::thread::sleep(std::time::Duration::from_secs(30)),
        _ => std::process::exit(23),
    }
}
