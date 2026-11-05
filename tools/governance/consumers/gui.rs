#![forbid(unsafe_code)]
use iced::{
    Element, Subscription, Task,
    widget::{button, column, container, operation, row, text, text_input},
};
use std::time::Duration;
#[derive(Default)]
struct App {
    busy: bool,
    pane: bool,
    graph: bool,
    detail: String,
    command: String,
    ticks: u64,
    layouts: u64,
    focused: bool,
    layout_checksum: f64,
}
#[derive(Clone, Debug)]
enum Msg {
    Slow,
    Done,
    Pane,
    Graph,
    Quit,
    Tick,
    Focus(bool),
    Detail(String),
    Command(String),
}
impl App {
    fn boot() -> (Self, Task<Msg>) {
        (
            Self {
                pane: true,
                ..Self::default()
            },
            operation::focus("detail"),
        )
    }
    fn update(&mut self, m: Msg) -> Task<Msg> {
        match m {
            Msg::Slow if !self.busy => {
                self.busy = true;
                let (tx, rx) = iced::futures::channel::oneshot::channel();
                std::thread::spawn(move || {
                    std::thread::sleep(Duration::from_secs(3));
                    let _ = tx.send(());
                });
                return Task::perform(async move { rx.await.expect("worker dropped") }, |_| {
                    Msg::Done
                });
            }
            Msg::Done => self.busy = false,
            Msg::Pane => {
                self.pane = !self.pane;
                self.focused = false;
                return operation::focus(if self.pane { "detail" } else { "command" });
            }
            Msg::Graph => self.graph = !self.graph,
            Msg::Quit => return iced::exit(),
            Msg::Tick => {
                self.ticks += 1;
                if self.graph {
                    self.relayout();
                }
                return operation::is_focused(if self.pane { "detail" } else { "command" })
                    .map(Msg::Focus);
            }
            Msg::Focus(v) => self.focused = v,
            Msg::Detail(s) => self.detail = s,
            Msg::Command(s) => self.command = s,
            _ => {}
        }
        Task::none()
    }
    fn relayout(&mut self) {
        let mut sum = 0.0;
        for n in 0..10000 {
            sum += (n as f64).sin();
        }
        self.layout_checksum = sum;
        self.layouts += 1;
    }
    fn title(&self) -> String {
        format!(
            "consumer|ticks={}|busy={}|pane={}|graph={}|focus={}|detail={}|command={}|layouts={}",
            self.ticks,
            u8::from(self.busy),
            u8::from(self.pane),
            u8::from(self.graph),
            u8::from(self.focused),
            self.detail,
            self.command,
            self.layouts
        )
    }
    fn view(&self) -> Element<'_, Msg> {
        let mut content = column![
            row![
                button(text("Slow").size(14)).width(52).on_press(Msg::Slow),
                button(text("Pane").size(14)).width(52).on_press(Msg::Pane),
                button(text("Graph").size(14))
                    .width(52)
                    .on_press(Msg::Graph),
                button(text("Quit").size(14)).width(52).on_press(Msg::Quit)
            ]
            .spacing(4),
            text_input("Command", &self.command)
                .id("command")
                .on_input(Msg::Command)
        ]
        .spacing(8);
        if self.pane {
            content = content.push(
                text_input("Retained detail", &self.detail)
                    .id("detail")
                    .on_input(Msg::Detail),
            );
        }
        content = content.push(text(if self.busy { "Worker running" } else { "Ready" }));
        if self.graph {
            content = content.push(text(format!(
                "Graph layout {} ({:.2})",
                self.layouts, self.layout_checksum
            )));
        }
        container(content).padding(8).into()
    }
}
fn main() -> iced::Result {
    iced::application(App::boot, App::update, App::view)
        .title(App::title)
        .window_size((600., 400.))
        .subscription(|_| Subscription::run(ticks))
        .run()
}
fn ticks() -> impl iced::futures::Stream<Item = Msg> {
    let (mut tx, rx) = iced::futures::channel::mpsc::channel(1);
    std::thread::spawn(move || {
        loop {
            std::thread::sleep(Duration::from_millis(40));
            if let Err(e) = tx.try_send(Msg::Tick) {
                if e.is_disconnected() {
                    break;
                }
            }
        }
    });
    rx
}
