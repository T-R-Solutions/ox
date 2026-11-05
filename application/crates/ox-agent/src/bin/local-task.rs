//! Controlled artifact producer; runs only in a newly owned attempt directory.
#![forbid(unsafe_code)]
use std::{
    fs::{self, OpenOptions},
    io::{self, Write},
};
fn run() -> io::Result<()> {
    let mode = std::env::args().nth(1).unwrap_or_default();
    if mode == "failure" {
        return Err(io::Error::other("controlled failure"));
    }
    if mode == "hang" {
        std::thread::sleep(std::time::Duration::from_secs(30));
        return Ok(());
    }
    if !matches!(mode.as_str(), "good" | "bad") {
        return Err(io::Error::other("unknown mode"));
    }
    let request = fs::read_to_string("request.txt")?;
    if request.len() > 256 || !request.starts_with("ox-task-v1:") {
        return Err(io::Error::other("invalid request"));
    }
    let mut output = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open("result.txt")?;
    output.write_all(request.as_bytes())?;
    output.write_all(if mode == "good" {
        b"result=42\n"
    } else {
        b"result=41\n"
    })?;
    output.sync_all()
}
fn main() {
    if let Err(error) = run() {
        eprintln!("{error}");
        std::process::exit(17);
    }
}
