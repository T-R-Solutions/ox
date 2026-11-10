#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Termination {
    ExitCode(i32),
    Signal(i32),
    Unknown,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Completeness {
    Complete,
    Incomplete { reason: String },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RawOutput {
    pub stdout: Vec<u8>,
    pub stderr: Vec<u8>,
    pub termination: Termination,
    pub completeness: Completeness,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Projection {
    pub text: String,
    pub losses: Vec<String>,
    pub original: RawOutput,
}
