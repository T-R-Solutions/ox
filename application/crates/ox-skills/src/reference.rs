#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SelectionState {
    Available,
    Suggested,
    Selected,
    Consulted,
    Used,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SkillReference {
    pub name: String,
    pub entry: std::path::PathBuf,
    pub state: SelectionState,
}
