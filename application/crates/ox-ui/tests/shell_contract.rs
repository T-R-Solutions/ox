use ox_ui::shell::{Effect, Message, Shell};
#[test]
fn exit_requests_runtime_shutdown_without_changing_presentation() {
    let mut shell = Shell::default();
    shell.update(Message::ToggleDetails);
    assert_eq!(shell.update(Message::Exit), Effect::Exit);
    assert!(shell.details_visible());
}
