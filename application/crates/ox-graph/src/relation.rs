#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NodeKey(pub String);
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RelationshipEvidence {
    Verified {
        method: String,
        snapshot: String,
        source: String,
    },
    Inferred {
        method: String,
        snapshot: String,
        source: String,
    },
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Relation {
    pub from: NodeKey,
    pub to: NodeKey,
    pub kind: String,
    pub evidence: RelationshipEvidence,
}
