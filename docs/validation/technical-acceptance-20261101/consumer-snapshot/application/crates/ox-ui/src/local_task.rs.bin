//! Local task controller. Invoke blocking methods only on a worker.
use ox_agent::runtime::{Identity, Runtime, State};
use ox_verification::{
    engine::{Check, Engine},
    verdict::Verdict,
};
use std::{
    fs::{self, OpenOptions},
    io::{self, Write},
    path::{Path, PathBuf},
    sync::{
        Arc,
        atomic::{AtomicBool, Ordering},
    },
    time::{Duration, SystemTime, UNIX_EPOCH},
};
pub struct Controller {
    pub workspace: Option<PathBuf>,
    pub attempt: u64,
    session: u128,
    binaries: PathBuf,
    engine: Engine,
    check: Option<Check>,
}
impl Controller {
    pub fn new(binaries: PathBuf) -> Self {
        Self {
            workspace: None,
            attempt: 0,
            session: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap_or_default()
                .as_nanos(),
            binaries,
            engine: Engine::default(),
            check: None,
        }
    }
    pub fn select(&mut self, path: &Path) -> io::Result<String> {
        let root = path.canonicalize()?;
        if !root.is_dir() {
            return Err(io::Error::other("Not a directory"));
        }
        fs::read_dir(&root)?;
        self.workspace = Some(root.clone());
        self.check = None;
        Ok(format!("Workspace: {} — UNVERIFIED", root.display()))
    }
    pub fn execute(&mut self, mode: &str, cancel: Arc<AtomicBool>) -> io::Result<String> {
        if !matches!(mode, "good" | "bad" | "failure" | "hang") {
            return Err(io::Error::other("Unknown scenario"));
        }
        let root = self
            .workspace
            .as_ref()
            .ok_or_else(|| io::Error::other("Select workspace"))?;
        fs::read_dir(root)?;
        self.attempt += 1;
        let id = format!("{}:1:{}", self.session, self.attempt);
        let dir = root.join(format!(".ox-task-{}-{}", self.session, self.attempt));
        fs::create_dir(&dir)?;
        let mut request = OpenOptions::new()
            .write(true)
            .create_new(true)
            .open(dir.join("request.txt"))?;
        writeln!(request, "ox-task-v1:{id}")?;
        request.sync_all()?;
        self.check = Some(Check {
            id: format!("result:{id}"),
            description: "Identity and result=42".into(),
            executable: self.binaries.join("task-oracle"),
            arguments: vec![id],
            directory: dir.clone(),
            inputs: vec![
                dir.join("request.txt"),
                dir.join("result.txt"),
                self.binaries.join("local-task"),
            ],
            expected_exit: 0,
        });
        let mut runtime = Runtime::spawn(
            &self.binaries.join("local-task"),
            mode,
            &dir,
            Identity {
                session: std::process::id() as u64,
                task: 1,
                attempt: self.attempt,
            },
            Duration::from_secs(10),
        )?;
        loop {
            if cancel.load(Ordering::Relaxed) {
                runtime.cancel()?;
            }
            if let State::Finished(outcome) = runtime.poll()? {
                let result_note = if dir.join("result.txt").is_file() {
                    "Result produced. Choose Verify result before starting another attempt."
                } else {
                    "No result was produced; verification cannot approve missing evidence. Start a new attempt."
                };
                return Ok(format!(
                    "Attempt {}: {outcome:?}; observed exit. {}. UNVERIFIED. {result_note}",
                    self.attempt,
                    dir.display()
                ));
            }
            std::thread::sleep(Duration::from_millis(10));
        }
    }
    pub fn verify(&mut self, execute: bool) -> io::Result<String> {
        let check = self
            .check
            .as_ref()
            .ok_or_else(|| io::Error::other("No result"))?;
        if execute {
            for path in check
                .inputs
                .iter()
                .chain(std::iter::once(&check.executable))
            {
                if !path.is_file() {
                    return Err(io::Error::new(
                        io::ErrorKind::NotFound,
                        format!(
                            "Attempt {} has no readable regular evidence input: {}. No approval is possible. Verify immediately after Run correct or Run incorrect; Fail, Timeout and Cancel may produce no result.",
                            self.attempt,
                            path.display()
                        ),
                    ));
                }
            }
            self.engine
                .execute(check, Duration::from_secs(10))
                .map_err(|error| {
                    io::Error::new(
                        error.kind(),
                        format!("Verification of {} could not complete: {error}", check.id),
                    )
                })?;
        }
        let verdict = self.engine.evaluate(check);
        let status = match verdict {
            Verdict::Approved { .. } => "APPROVED",
            Verdict::Rejected { .. } => "REJECTED",
            Verdict::NotVerified => "UNVERIFIED / stale or missing",
            Verdict::Inconclusive { .. } => "INCONCLUSIVE",
            Verdict::NotApplicable { .. } => "NOT APPLICABLE",
        };
        let history = self
            .engine
            .observations()
            .iter()
            .map(|o| {
                let contents = o
                    .inputs()
                    .iter()
                    .filter(|input| input.bytes.len() <= 256)
                    .map(|input| {
                        format!(
                            "{}: {:?}",
                            input.path.display(),
                            String::from_utf8_lossy(&input.bytes)
                        )
                    })
                    .collect::<Vec<_>>()
                    .join("; ");
                format!(
                    "run {}: {} {:?}; {} inputs; recorded content: {contents}",
                    o.run(),
                    o.check().id,
                    o.result(),
                    o.inputs().len()
                )
            })
            .collect::<Vec<_>>()
            .join("\n");
        Ok(format!(
            "{status}\nCriterion: {}\n{verdict:?}\nObserved {:?}; refresh explicitly after edits.\nInputs: {:?}\nOracle: {} {:?}\nHistory:\n{history}",
            check.id,
            SystemTime::now(),
            check.inputs,
            check.executable.display(),
            check.arguments
        ))
    }
}
