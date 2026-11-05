//! Controlled local test process, not an installed plugin or sandbox.
#![forbid(unsafe_code)]
use std::{
    io::{BufRead, BufReader, Write},
    os::unix::net::UnixStream,
    time::Duration,
};
fn main() -> std::io::Result<()> {
    let args: Vec<_> = std::env::args().collect();
    let mut stream = UnixStream::connect(&args[1])?;
    let mode = args[2].as_str();
    writeln!(
        stream,
        "HELLO {} 0 {}",
        if mode == "incompatible" { "2" } else { "1" },
        if mode == "unsupported" { "-" } else { "echo" }
    )?;
    let mut reader = BufReader::new(stream.try_clone()?);
    let mut line = String::new();
    reader.read_line(&mut line)?;
    loop {
        line.clear();
        if reader.read_line(&mut line)? == 0 {
            return Ok(());
        }
        if line == "STOP\n" {
            return Ok(());
        }
        match mode {
            "denied" | "unsupported" => std::process::exit(21),
            "crash" => std::process::exit(22),
            "timeout" => std::thread::sleep(Duration::from_secs(30)),
            "malformed" => writeln!(stream, "NOT-A-RESPONSE")?,
            "oversized" => writeln!(stream, "{}", "x".repeat(1025))?,
            "mismatch" => writeln!(stream, "OK 999 wrong")?,
            _ => {
                let fields: Vec<_> = line.trim_end().split(' ').collect();
                if fields.len() != 4 || fields[0] != "CALL" || fields[2] != "echo" {
                    std::process::exit(23);
                }
                writeln!(stream, "OK {} {}", fields[1], fields[3])?;
            }
        }
    }
}
