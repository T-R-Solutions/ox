#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SessionState {
    NotStarted,
    Running,
    Cancelling,
    Exited { code: Option<i32> },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SessionCapabilities {
    pub cancellation: bool,
    pub usage_reporting: bool,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SessionError {
    AdapterUnavailable,
    InvalidTransition,
}
