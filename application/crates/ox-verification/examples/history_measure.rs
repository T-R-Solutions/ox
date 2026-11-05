//! Measures the documented maximum retained history envelope, without a GUI.
#![forbid(unsafe_code)]
use ox_verification::engine::{Check, Engine};
use std::{
    fs,
    path::PathBuf,
    time::{Duration, Instant},
};
fn main() {
    let root = PathBuf::from(std::env::args().nth(1).expect("fresh corpus directory"));
    fs::create_dir(&root).unwrap();
    let executable = PathBuf::from(std::env::args().nth(2).expect("local oracle path"));
    let mut inputs = Vec::new();
    for i in 0..2 {
        let p = root.join(i.to_string());
        fs::File::create(&p)
            .unwrap()
            .set_len(15 * 1024 * 1024)
            .unwrap();
        inputs.push(p);
    }
    let check = Check {
        id: "max-history".into(),
        description: "controlled rejected history memory".into(),
        executable,
        arguments: vec![inputs[0].to_str().unwrap().into()],
        directory: root,
        inputs,
        expected_exit: 0,
    };
    let mut e = Engine::default();
    let start = Instant::now();
    for _ in 0..32 {
        if let Err(error) = e.execute(&check, Duration::from_secs(2)) {
            println!("admission_refused={error}");
            break;
        }
    }
    println!(
        "observations={},elapsed_ms={:.3},before_payload_bytes={}",
        e.observations().len(),
        start.elapsed().as_secs_f64() * 1000.,
        e.observations()
            .iter()
            .flat_map(|o| o.inputs())
            .map(|i| i.bytes.len())
            .sum::<usize>()
    );
    assert!(e.execute(&check, Duration::from_secs(2)).is_err());
    assert_eq!(e.observations().len(), 2);
}
