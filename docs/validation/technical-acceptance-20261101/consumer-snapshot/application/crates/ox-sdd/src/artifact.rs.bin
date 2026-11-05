#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ArtifactKind {
    Spec,
    Plan,
    Tasks,
    Convergence,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Artifact {
    pub kind: ArtifactKind,
    pub path: std::path::PathBuf,
}
#[derive(Debug)]
pub enum ReadError {
    ReaderUnavailable,
    Io(std::io::Error),
    InvalidFormat { reason: String },
}
