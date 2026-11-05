//! Controlled oracle: literal accepted bytes are independent of Engine verdict logic.
#![forbid(unsafe_code)]
fn main() {
    let arg = std::env::args().nth(1).expect("candidate path");
    if arg == "flip" {
        // Deliberately uncontrolled test dependency: provoke contradictory observations.
        let marker = std::env::args().nth(2).expect("marker path");
        if !std::path::Path::new(&marker).exists() {
            std::fs::write(marker, b"first failure").unwrap();
            std::process::exit(17);
        }
        return;
    }
    if arg == "hang" {
        std::thread::sleep(std::time::Duration::from_secs(30));
        return;
    }
    if !matches!(std::fs::read(arg).as_deref(), Ok(b"accepted\n")) {
        std::process::exit(17);
    }
}
