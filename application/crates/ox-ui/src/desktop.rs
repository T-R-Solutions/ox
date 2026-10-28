use crate::shell::{Effect, Message, Shell};
use iced::widget::{button, column, container, text};
use iced::{Element, Task};
pub type Result = iced::Result;

pub fn run() -> Result {
    iced::application(Shell::default, update, view)
        .title(|shell: &Shell| {
            if shell.details_visible() {
                "Ox — Fundação • detalhes".to_owned()
            } else {
                "Ox — Fundação".to_owned()
            }
        })
        .window_size((640.0, 360.0))
        .run()
}
fn update(shell: &mut Shell, message: Message) -> Task<Message> {
    match shell.update(message) {
        Effect::None => Task::none(),
        Effect::Exit => iced::exit(),
    }
}
fn view(shell: &Shell) -> Element<'_, Message> {
    let mut content = column![
        text("Ox").size(32),
        text("Fundação local • F0"),
        button(if shell.details_visible() {
            "Ocultar detalhes"
        } else {
            "Mostrar detalhes"
        })
        .on_press(Message::ToggleDetails)
    ]
    .spacing(16);
    if shell.details_visible() {
        content = content.push(text(
            "16 módulos definidos. Agentes, plugins e armazenamento ainda indisponíveis.",
        ));
    }
    container(content.push(button("Sair").on_press(Message::Exit)))
        .padding(24)
        .into()
}
