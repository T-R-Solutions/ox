//! Local F0 measurement harness; no acceptance thresholds are implied by these samples.
#![forbid(unsafe_code)]
use ox_agent::runtime::{Identity, Runtime, State};
use ox_ui::local_task::Controller;
use ox_verification::engine::{Check, Engine, ResultKind};
use std::{
    fs,
    path::PathBuf,
    sync::{
        Arc,
        atomic::{AtomicBool, Ordering},
    },
    time::{Duration, Instant},
};
fn main() {
    let binaries = PathBuf::from(
        std::env::args()
            .nth(1)
            .expect("absolute fixture bin directory"),
    );
    let root = PathBuf::from(std::env::args().nth(2).expect("fresh corpus directory"));
    fs::create_dir(&root).unwrap();
    println!("iteration,execute_ms,verify_ms,runtime_cancel_exit_ms,verify_cancel_exit_ms");
    for iteration in 0..23 {
        let directory = root.join(iteration.to_string());
        fs::create_dir(&directory).unwrap();
        let mut controller = Controller::new(binaries.clone());
        controller.select(&directory).unwrap();
        let start = Instant::now();
        assert!(
            controller
                .execute("good", Arc::new(AtomicBool::new(false)))
                .unwrap()
                .contains("Success")
        );
        let execution = start.elapsed();
        let start = Instant::now();
        assert!(controller.verify(true).unwrap().starts_with("APPROVED"));
        let verification = start.elapsed();
        let mut runtime = Runtime::spawn(
            &binaries.join("local-agent"),
            "hang",
            &directory,
            Identity {
                session: 1,
                task: 1,
                attempt: iteration + 1,
            },
            Duration::from_secs(2),
        )
        .unwrap();
        let pid = runtime.pid();
        let start = Instant::now();
        runtime.cancel().unwrap();
        while !matches!(runtime.poll().unwrap(), State::Finished(_)) {
            std::thread::yield_now();
        }
        let runtime_cancel = start.elapsed();
        assert!(!PathBuf::from(format!("/proc/{pid}")).exists());
        let ready = directory.join("ready");
        let check = Check {
            id: "cancel-benchmark".into(),
            description: "controlled cancellation".into(),
            executable: binaries.join("local-oracle"),
            arguments: vec!["barrier".into(), ready.to_str().unwrap().into()],
            directory: directory.clone(),
            inputs: vec![binaries.join("task-oracle")],
            expected_exit: 0,
        };
        let cancel = Arc::new(AtomicBool::new(false));
        let flag = cancel.clone();
        let worker = std::thread::spawn(move || {
            let mut engine = Engine::default();
            engine
                .execute_cancellable(&check, Duration::from_secs(2), &flag)
                .unwrap();
            engine
        });
        let until = Instant::now() + Duration::from_secs(5);
        let oracle_pid = loop {
            if let Ok(text) = fs::read_to_string(&ready)
                && let Ok(pid) = text.parse::<u32>()
            {
                break pid;
            }
            assert!(Instant::now() < until);
            std::thread::yield_now();
        };
        let start = Instant::now();
        cancel.store(true, Ordering::Relaxed);
        let engine = worker.join().unwrap();
        let verify_cancel = start.elapsed();
        assert_eq!(engine.observations()[0].result(), ResultKind::Cancelled);
        assert!(!PathBuf::from(format!("/proc/{oracle_pid}")).exists());
        if iteration >= 3 {
            println!(
                "{},{:.6},{:.6},{:.6},{:.6}",
                iteration - 3,
                execution.as_secs_f64() * 1000.,
                verification.as_secs_f64() * 1000.,
                runtime_cancel.as_secs_f64() * 1000.,
                verify_cancel.as_secs_f64() * 1000.
            );
        }
    }
}
