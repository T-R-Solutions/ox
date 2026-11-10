#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum TaskState {
    #[default]
    Planned,
    Running,
    Cancelled,
    Failed,
    Completed,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct InvalidTransition;
impl TaskState {
    pub fn transition(&mut self, next: Self) -> Result<(), InvalidTransition> {
        if matches!(
            (*self, next),
            (Self::Planned, Self::Running | Self::Cancelled)
                | (
                    Self::Running,
                    Self::Cancelled | Self::Failed | Self::Completed
                )
        ) {
            *self = next;
            Ok(())
        } else {
            Err(InvalidTransition)
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rejected_transition_preserves_state() {
        let mut s = TaskState::Planned;
        assert_eq!(s.transition(TaskState::Completed), Err(InvalidTransition));
        assert_eq!(s, TaskState::Planned);
    }
}
