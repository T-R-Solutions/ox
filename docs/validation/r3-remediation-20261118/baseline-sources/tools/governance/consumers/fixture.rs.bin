#![forbid(unsafe_code)]
#[allow(dead_code)]
mod operations;
#[allow(dead_code)]
mod plugin_host;
use std::{io::Write, path::Path};
fn main() {
    let args: Vec<_> = std::env::args().collect();
    match args.get(1).map(String::as_str) {
        Some("edit") => {
            let r = operations::edit(
                Path::new(&args[2]),
                Path::new("target"),
                b"base",
                args[3].as_bytes(),
                args[3] == "crash",
            );
            match r {
                Ok(()) => {}
                Err(e) => {
                    eprintln!("{e}");
                    std::process::exit(23)
                }
            }
        }
        Some("stream") => {
            let err = std::thread::spawn(|| {
                let mut s = std::io::stderr().lock();
                let b = [b'e'; 8192];
                loop {
                    s.write_all(&b).unwrap();
                }
            });
            let mut s = std::io::stdout().lock();
            let b = [b'o'; 8192];
            for _ in 0..usize::MAX {
                s.write_all(&b).unwrap();
            }
            err.join().unwrap();
        }
        Some("plugin-check") => {
            use plugin_host::{Error, Host};
            use std::time::Duration;
            let bin = Path::new(&args[2]);
            assert!(matches!(
                Host::start(bin, "incompatible", true, Duration::from_millis(500)),
                Err(Error::Incompatible)
            ));
            {
                let mut host =
                    Host::start(bin, "malformed", true, Duration::from_millis(500)).unwrap();
                let socket = host.socket_directory().to_owned();
                assert_eq!(host.echo("data"), Err(Error::InvalidFrame));
                drop(host);
                assert!(!socket.exists());
            }
            let prefix = format!("ox-plugin-{}-", std::process::id());
            assert!(!std::fs::read_dir(std::env::temp_dir()).unwrap().any(|x| {
                x.unwrap()
                    .file_name()
                    .to_string_lossy()
                    .starts_with(&prefix)
            }));
            println!("incompatible and malformed rejected; transport directories removed");
        }
        Some("read") => match std::fs::read(&args[2]) {
            Ok(bytes) => std::io::stdout().write_all(&bytes).unwrap(),
            Err(e) => {
                eprintln!("READ_DENIED {:?}", e.kind());
                std::process::exit(13)
            }
        },
        _ => std::process::exit(2),
    }
}
