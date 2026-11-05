use crate::local_task::Controller;
use iced::{
    Element, Task,
    widget::{button, column, container, row, scrollable, text, text_input},
};
use std::{
    path::PathBuf,
    sync::{
        Arc, Mutex,
        atomic::{AtomicBool, Ordering},
    },
};
pub type Result = iced::Result;
struct Desktop {
    controller: Arc<Mutex<Controller>>,
    cancel: Arc<AtomicBool>,
    path: String,
    selected: bool,
    result: bool,
    busy: bool,
    closing: bool,
    generation: u64,
    status: String,
    details: bool,
}
impl Default for Desktop {
    fn default() -> Self {
        let binaries = std::env::current_exe()
            .ok()
            .and_then(|p| p.parent().map(PathBuf::from))
            .unwrap_or_default();
        Self {
            controller: Arc::new(Mutex::new(Controller::new(binaries))),
            cancel: Arc::new(AtomicBool::new(false)),
            path: String::new(),
            selected: false,
            result: false,
            busy: false,
            closing: false,
            generation: 0,
            status:
                "UNVERIFIED. Controlled fixture; no sandbox, remote agents or persisted history."
                    .into(),
            details: false,
        }
    }
}
#[derive(Clone, Debug)]
enum Message {
    Path(String),
    Select,
    Start(&'static str),
    Verify,
    Refresh,
    Cancel,
    Close,
    Toggle,
    Done(u64, Action, std::result::Result<String, String>),
}
#[derive(Clone, Copy, Debug)]
enum Action {
    Select,
    Start,
    Verify,
    Refresh,
}
impl Desktop {
    fn launch(&mut self, action: Action, mode: &'static str) -> Task<Message> {
        if self.busy || self.closing {
            return Task::none();
        }
        self.busy = true;
        self.generation += 1;
        let generation = self.generation;
        self.cancel.store(false, Ordering::Relaxed);
        self.status = match action {
            Action::Start => "Running controlled task; deadline 10 seconds. Cancel requests termination before timeout.",
            Action::Verify => "Verifying the current attempt; deadline 10 seconds…",
            Action::Refresh => "Observing current inputs…",
            Action::Select => "Validating workspace…",
        }.into();
        let controller = self.controller.clone();
        let cancel = self.cancel.clone();
        let path = self.path.clone();
        let (send, receive) = iced::futures::channel::oneshot::channel();
        let spawn = std::thread::Builder::new()
            .name("ox-local-task".into())
            .spawn(move || {
                let result = controller
                    .lock()
                    .map_err(|_| "Worker state unavailable".to_owned())
                    .and_then(|mut c| {
                        match action {
                            Action::Select => c.select(&PathBuf::from(path)),
                            Action::Start => c.execute(mode, cancel),
                            Action::Verify => c.verify(true),
                            Action::Refresh => c.verify(false),
                        }
                        .map_err(|e| e.to_string())
                    });
                let _ = send.send(result);
            });
        if let Err(e) = spawn {
            self.busy = false;
            self.status = e.to_string();
            return Task::none();
        }
        Task::perform(
            async move {
                receive
                    .await
                    .unwrap_or_else(|_| Err("Worker terminated unexpectedly".into()))
            },
            move |result| Message::Done(generation, action, result),
        )
    }
    fn update(&mut self, message: Message) -> Task<Message> {
        match message {
            Message::Toggle => self.details = !self.details,
            Message::Path(path) if !self.busy => {
                self.generation += 1;
                self.path = path;
                self.selected = false;
                self.result = false;
                self.status = "UNVERIFIED — validate workspace".into();
            }
            Message::Select if !self.busy => {
                self.selected = false;
                self.result = false;
                return self.launch(Action::Select, "");
            }
            Message::Start(mode) if self.selected && !self.busy => {
                self.result = false;
                return self.launch(Action::Start, mode);
            }
            Message::Verify if self.result => return self.launch(Action::Verify, ""),
            Message::Refresh if self.result => return self.launch(Action::Refresh, ""),
            Message::Cancel if self.busy => {
                self.cancel.store(true, Ordering::Relaxed);
                self.status="Cancellation requested; awaiting observed termination. Verification finishes under its deadline.".into();
            }
            Message::Close => {
                self.closing = true;
                self.cancel.store(true, Ordering::Relaxed);
                if !self.busy {
                    return iced::exit();
                }
                self.status = "Closing: awaiting owned work termination…".into();
            }
            Message::Done(g, action, result) if g == self.generation && self.busy => {
                self.busy = false;
                if matches!(action, Action::Select) {
                    self.selected = result.is_ok();
                }
                if matches!(action, Action::Start) {
                    self.result = result.is_ok();
                }
                self.status = result.unwrap_or_else(|e| format!("UNVERIFIED — {e}"));
                if self.closing {
                    return iced::exit();
                }
            }
            _ => {}
        }
        Task::none()
    }
    fn view(&self) -> Element<'_, Message> {
        let available = !self.busy && !self.closing;
        let start = available && self.selected;
        let verify = available && self.result;
        let mut content = column![
            text("Ox").size(32),
            text("Fundação local • F0"),
            button(if self.details {
                "Ocultar detalhes"
            } else {
                "Mostrar detalhes"
            })
            .on_press(Message::Toggle)
        ]
        .spacing(16);
        if self.details {
            content = content.push(text(
                "Controlled local task and independent verification. No remote agents or sandbox.",
            ));
        }
        content = content.push(button("Sair").on_press(Message::Close));
        let input = text_input("Existing workspace path", &self.path);
        content = content.push(if available {
            input.on_input(Message::Path)
        } else {
            input
        });
        content = content.push(
            button("Validate workspace").on_press_maybe(available.then_some(Message::Select)),
        );
        content = content.push(
            row![
                button("Run correct").on_press_maybe(start.then_some(Message::Start("good"))),
                button("Run incorrect").on_press_maybe(start.then_some(Message::Start("bad"))),
                button("Fail").on_press_maybe(start.then_some(Message::Start("failure"))),
                button("Timeout").on_press_maybe(start.then_some(Message::Start("hang")))
            ]
            .spacing(8),
        );
        content = content.push(
            row![
                button("Cancel").on_press_maybe(self.busy.then_some(Message::Cancel)),
                button("Verify result").on_press_maybe(verify.then_some(Message::Verify)),
                button("Refresh inputs").on_press_maybe(verify.then_some(Message::Refresh))
            ]
            .spacing(8),
        );
        container(scrollable(content.push(text(&self.status))))
            .padding(24)
            .into()
    }
}
pub fn run() -> Result {
    iced::application(Desktop::default, Desktop::update, Desktop::view)
        .title(|s: &Desktop| {
            if s.details {
                "Ox — Fundação • detalhes".to_owned()
            } else {
                "Ox — Fundação".to_owned()
            }
        })
        .window_size((900.0, 700.0))
        .exit_on_close_request(false)
        .subscription(|_| iced::window::close_requests().map(|_| Message::Close))
        .run()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn busy_and_stale_events_do_not_change_identity_or_workspace() {
        let mut ui = Desktop {
            busy: true,
            selected: true,
            generation: 4,
            path: "/original".into(),
            ..Desktop::default()
        };
        let _ = ui.update(Message::Path("/other".into()));
        let _ = ui.update(Message::Start("good"));
        let _ = ui.update(Message::Verify);
        let _ = ui.update(Message::Done(3, Action::Select, Ok("old".into())));
        assert_eq!(ui.path, "/original");
        assert_eq!(ui.generation, 4);
        assert!(ui.busy);
        let _ = ui.update(Message::Cancel);
        assert!(ui.busy);
        assert!(ui.cancel.load(Ordering::Relaxed));
        let _ = ui.update(Message::Toggle);
        assert!(ui.details);
        let _ = ui.update(Message::Close);
        assert!(ui.closing);
        assert!(ui.busy);
        let _ = ui.update(Message::Done(
            4,
            Action::Start,
            Ok("Cancelled; observed exit".into()),
        ));
        assert!(!ui.busy);
        let _ = ui.update(Message::Done(4, Action::Select, Ok("duplicate".into())));
        assert_ne!(ui.status, "duplicate");
        ui.closing = false;
        let _ = ui.update(Message::Path("/new".into()));
        let _ = ui.update(Message::Done(
            4,
            Action::Select,
            Ok("late workspace".into()),
        ));
        assert!(!ui.selected);
        assert_eq!(ui.path, "/new");
    }
}
