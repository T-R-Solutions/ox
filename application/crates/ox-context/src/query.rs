#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContextQuery {
    pub text: String,
    pub limit: std::num::NonZeroUsize,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ContextHit {
    pub path: std::path::PathBuf,
    pub snapshot: String,
    pub excerpt: String,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum QueryError {
    IndexUnavailable,
    StaleSnapshot,
}
