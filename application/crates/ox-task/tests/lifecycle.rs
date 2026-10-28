use ox_task::state::TaskState;
#[test]
fn terminal_states_cannot_restart() {
    for end in [
        TaskState::Cancelled,
        TaskState::Failed,
        TaskState::Completed,
    ] {
        let mut s = TaskState::Planned;
        s.transition(TaskState::Running).unwrap();
        s.transition(end).unwrap();
        assert!(s.transition(TaskState::Running).is_err());
        assert_eq!(s, end);
    }
}
