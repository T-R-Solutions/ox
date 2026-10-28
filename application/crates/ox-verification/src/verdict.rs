#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub enum Verdict {
    #[default]
    NotVerified,
    Approved {
        evidence: String,
    },
    Rejected {
        evidence: String,
    },
    Inconclusive {
        reason: String,
    },
    NotApplicable {
        reason: String,
    },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Criterion {
    pub id: String,
    pub description: String,
    pub oracle: String,
    pub verdict: Verdict,
}
