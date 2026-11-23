//! Local task controller. Invoke blocking methods only on a worker.
use ox_agent::runtime::{Identity, Outcome, Runtime, State};
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
    #[must_use]
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
    /// # Errors
    /// Returns a filesystem error for a missing, unreadable or non-directory workspace.
    pub fn select(&mut self, path: &Path) -> io::Result<String> {
        let root = path.canonicalize()?;
        if !root.is_dir() {
            return Err(io::Error::other("O caminho não é um diretório"));
        }
        fs::read_dir(&root)?;
        self.workspace = Some(root.clone());
        self.check = None;
        Ok(format!("Projeto: {} — não verificado", root.display()))
    }
    /// # Errors
    /// Returns an error for an unknown scenario, absent workspace, filesystem failure, or child supervision failure.
    #[expect(
        clippy::needless_pass_by_value,
        reason = "Worker entry takes ownership of its cancellation handle"
    )]
    pub fn execute(&mut self, mode: &str, cancel: Arc<AtomicBool>) -> io::Result<String> {
        if !matches!(mode, "good" | "bad" | "failure" | "hang") {
            return Err(io::Error::other("Cenário desconhecido"));
        }
        let root = self
            .workspace
            .as_ref()
            .ok_or_else(|| io::Error::other("Selecione um projeto"))?;
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
            description: "Identidade e resultado=42".into(),
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
                session: u64::from(std::process::id()),
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
                return Ok(attempt_message(
                    self.attempt,
                    outcome,
                    &dir,
                    dir.join("result.txt").is_file(),
                ));
            }
            std::thread::sleep(Duration::from_millis(10));
        }
    }
    /// # Errors
    /// Returns an error when no result is selected, inputs cannot be read, or verification fails to execute.
    pub fn verify(&mut self, execute: bool) -> io::Result<String> {
        self.verify_cancellable(execute, &AtomicBool::new(false))
    }
    /// # Errors
    /// Returns an error when no result is selected, inputs cannot be read, or verification fails to execute.
    pub fn verify_cancellable(&mut self, execute: bool, cancel: &AtomicBool) -> io::Result<String> {
        let check = self
            .check
            .as_ref()
            .ok_or_else(|| io::Error::other("Nenhum resultado"))?;
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
                            "A tentativa {} não tem uma entrada de evidência regular e legível: {}. Não é possível aprovar. Verifique logo após Executar correto ou Executar incorreto; Falha, Prazo excedido e Cancelar podem não produzir resultado.",
                            self.attempt,
                            path.display()
                        ),
                    ));
                }
            }
            self.engine
                .execute_cancellable(check, Duration::from_secs(10), cancel)
                .map_err(|error| {
                    io::Error::new(
                        error.kind(),
                        format!(
                            "Não foi possível concluir a verificação de {}: {error}",
                            check.id
                        ),
                    )
                })?;
        }
        let verdict = self.engine.evaluate(check);
        let status = match &verdict {
            Verdict::Approved { .. } => "Critério aprovado",
            Verdict::Rejected { .. } => "Critério reprovado",
            Verdict::NotVerified => "Não verificado / entradas alteradas ou ausentes",
            Verdict::Inconclusive { .. } => "Inconclusivo",
            Verdict::NotApplicable { .. } => "Não aplicável",
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
                    "execução {}: {} {}; {} entradas; conteúdo registrado: {contents}",
                    o.run(),
                    o.check().id,
                    observation_result(o.result()),
                    o.inputs().len()
                )
            })
            .collect::<Vec<_>>()
            .join("\n");
        Ok(format!(
            "{status}\nCritério: {}\nReferência: {}\nObservado em {:?}; atualize explicitamente após editar.\nEntradas: {:?}\nOráculo: {} {:?}\nHistórico:\n{history}",
            check.id,
            verdict_reference(&verdict),
            SystemTime::now(),
            check.inputs,
            check.executable.display(),
            check.arguments
        ))
    }
}

fn verdict_reference(verdict: &Verdict) -> &str {
    match verdict {
        Verdict::Approved { evidence } | Verdict::Rejected { evidence } => evidence,
        Verdict::Inconclusive { reason } | Verdict::NotApplicable { reason } => reason,
        Verdict::NotVerified => "Nenhuma evidência atual permite decidir o critério",
    }
}

fn observation_result(result: ox_verification::engine::ResultKind) -> String {
    use ox_verification::engine::ResultKind;
    match result {
        ResultKind::Exited(Some(code)) => format!("código de saída {code}"),
        ResultKind::Exited(None) => "encerramento sem código de saída".into(),
        ResultKind::TimedOut => "prazo excedido".into(),
        ResultKind::Cancelled => "cancelada".into(),
    }
}

fn attempt_message(attempt: u64, outcome: Outcome, directory: &Path, has_result: bool) -> String {
    let outcome = match outcome {
        Outcome::Success => "concluída com sucesso".to_owned(),
        Outcome::Failed(Some(code)) => format!("falhou (código de saída {code})"),
        Outcome::Failed(None) => "falhou sem código de saída".to_owned(),
        Outcome::Cancelled => "cancelada".to_owned(),
        Outcome::TimedOut => "prazo excedido".to_owned(),
    };
    let result_note = if has_result {
        "Resultado produzido. Escolha Verificar resultado antes de iniciar outra tentativa."
    } else {
        "Nenhum resultado foi produzido; a verificação não pode aprovar evidências ausentes. Inicie outra tentativa."
    };
    format!(
        "Tentativa {attempt}: {outcome}; encerramento observado. Artefatos: {}. Estado: não verificado. {result_note}",
        directory.display()
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn attempt_messages_translate_every_outcome_without_claiming_verification() {
        for (outcome, expected) in [
            (Outcome::Success, "concluída com sucesso"),
            (Outcome::Failed(Some(7)), "falhou (código de saída 7)"),
            (Outcome::Failed(None), "falhou sem código de saída"),
            (Outcome::Cancelled, "cancelada"),
            (Outcome::TimedOut, "prazo excedido"),
        ] {
            for has_result in [true, false] {
                let message = attempt_message(3, outcome, Path::new("artefatos"), has_result);
                assert!(message.starts_with("Tentativa 3:"));
                assert!(message.contains(expected));
                assert!(message.contains("Estado: não verificado"));
                assert_eq!(
                    crate::design::EvidenceState::from_status(&message),
                    crate::design::EvidenceState::Unverified
                );
                assert!(message.contains(if has_result {
                    "Resultado produzido"
                } else {
                    "Nenhum resultado foi produzido"
                }));
                for old in [
                    "Attempt",
                    "Success",
                    "Failed",
                    "Cancelled",
                    "TimedOut",
                    "observed exit",
                    "UNVERIFIED",
                    "No result",
                ] {
                    assert!(!message.contains(old));
                }
            }
        }
    }
}
