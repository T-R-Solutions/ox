#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub enum Decision {
    #[default]
    ApprovalRequired,
    Denied {
        reason: String,
    },
    Granted {
        scope: String,
    },
}
