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
    focus: Option<usize>,
    validation_label: Option<String>,
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
            focus: None,
            validation_label: std::env::var("OX_VALIDATION_SESSION").ok(),
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
    Focus(bool),
    Activate,
    Scroll(f32),
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
    // Visual/tab order. Iced 0.14 buttons do not implement native keyboard focus.
    fn controls(&self) -> Vec<(usize, Message)> {
        let mut controls = vec![(0, Message::Toggle), (1, Message::Close)];
        if !self.busy && !self.closing {
            controls.extend([(2, Message::Activate), (3, Message::Select)]);
            if self.selected {
                controls.extend([
                    (4, Message::Start("good")),
                    (5, Message::Start("bad")),
                    (6, Message::Start("failure")),
                    (7, Message::Start("hang")),
                ]);
            }
            if self.result {
                controls.extend([(9, Message::Verify), (10, Message::Refresh)]);
            }
        }
        if self.busy {
            controls.push((8, Message::Cancel));
        }
        controls.sort_by_key(|(index, _)| *index);
        controls
    }
    fn control<'a>(
        &self,
        index: usize,
        label: &'a str,
        message: Option<Message>,
    ) -> iced::widget::Button<'a, Message> {
        let focused = self.focus == Some(index);
        button(label)
            .on_press_maybe(message)
            .style(move |theme, status| {
                let mut style = button::primary(theme, status);
                if focused {
                    style.border.width = 3.0;
                    style.border.color = iced::Color::BLACK;
                }
                style
            })
    }
    fn launch(&mut self, action: Action, mode: &'static str) -> Task<Message> {
        if self.busy || self.closing {
            return Task::none();
        }
        self.busy = true;
        self.generation += 1;
        let generation = self.generation;
        self.cancel.store(false, Ordering::Relaxed);
        self.status = match action {
            Action::Start => "Running controlled task; subprocess deadline 10 seconds. Cancel requests termination before timeout.",
            Action::Verify => "Verifying the current attempt; subprocess deadline 10 seconds…",
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
                            Action::Verify => c.verify_cancellable(true, &cancel),
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
            Message::Scroll(y) => {
                return iced::widget::operation::scroll_by(
                    "main",
                    iced::widget::scrollable::AbsoluteOffset { x: 0.0, y },
                );
            }
            Message::Focus(backwards) => {
                let controls = self.controls();
                let position = controls.iter().position(|(id, _)| Some(*id) == self.focus);
                let next = match (position, backwards) {
                    (Some(p), false) => (p + 1) % controls.len(),
                    (Some(p), true) => (p + controls.len() - 1) % controls.len(),
                    (None, false) => 0,
                    (None, true) => controls.len() - 1,
                };
                self.focus = Some(controls[next].0);
                return iced::widget::operation::focus(if self.focus == Some(2) {
                    "workspace"
                } else {
                    "no-text-input"
                });
            }
            Message::Activate => {
                if let Some((_, action)) = self
                    .controls()
                    .into_iter()
                    .find(|(id, _)| Some(*id) == self.focus && *id != 2)
                {
                    return self.update(action);
                }
            }
            Message::Toggle => self.details = !self.details,
            Message::Path(path) if !self.busy => {
                self.generation += 1;
                self.path = path;
                self.focus = Some(2);
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
                self.status =
                    "Cancellation requested; awaiting observed termination of the owned process."
                        .into();
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
            self.control(
                0,
                if self.details {
                    "Ocultar detalhes"
                } else {
                    "Mostrar detalhes"
                },
                Some(Message::Toggle)
            )
        ]
        .spacing(16);
        if self.details {
            content = content.push(text(
                "Controlled local task and independent verification. No remote agents or sandbox.",
            ));
        }
        content = content.push(self.control(1, "Sair", Some(Message::Close)));
        let input = text_input("Existing workspace path", &self.path)
            .id("workspace")
            .style(|theme, status| {
                let mut style = text_input::default(theme, status);
                if status != text_input::Status::Disabled {
                    style.placeholder = iced::Color::from_rgb8(89, 89, 89);
                    style.border.color = iced::Color::from_rgb8(89, 89, 89);
                    if matches!(status, text_input::Status::Focused { .. }) {
                        style.border.color = iced::Color::BLACK;
                        style.border.width = 2.0;
                    }
                }
                style
            });
        content = content.push(if available {
            input.on_input(Message::Path).on_submit(Message::Select)
        } else {
            input
        });
        content = content.push(self.control(
            3,
            "Validate workspace",
            available.then_some(Message::Select),
        ));
        content = content.push(
            row![
                self.control(4, "Run correct", start.then_some(Message::Start("good"))),
                self.control(5, "Run incorrect", start.then_some(Message::Start("bad"))),
                self.control(6, "Fail", start.then_some(Message::Start("failure"))),
                self.control(7, "Timeout", start.then_some(Message::Start("hang")))
            ]
            .spacing(8)
            .wrap(),
        );
        content = content.push(
            row![
                self.control(8, "Cancel", self.busy.then_some(Message::Cancel)),
                self.control(9, "Verify result", verify.then_some(Message::Verify)),
                self.control(10, "Refresh inputs", verify.then_some(Message::Refresh))
            ]
            .spacing(8)
            .wrap(),
        );
        container(scrollable(content.push(text(&self.status))).id("main"))
            .padding(24)
            .into()
    }
}
pub fn run() -> Result {
    iced::application(Desktop::default, Desktop::update, Desktop::view)
        .title(|s: &Desktop| {
            let title = if s.details {
                "Ox — Fundação • detalhes".to_owned()
            } else {
                "Ox — Fundação".to_owned()
            };
            if let Some(label) = &s.validation_label {
                format!("{title} [{label}]")
            } else {
                title
            }
        })
        .window_size((900.0, 700.0))
        .theme(iced::Theme::Light)
        .exit_on_close_request(false)
        .subscription(|_| {
            iced::Subscription::batch([
                iced::window::close_requests().map(|_| Message::Close),
                iced::event::listen_with(|event, status, _| {
                    if let iced::Event::Keyboard(iced::keyboard::Event::KeyPressed {
                        key,
                        modifiers,
                        ..
                    }) = event
                    {
                        use iced::keyboard::{Key, key::Named};
                        return match key {
                            Key::Named(Named::Tab) => Some(Message::Focus(modifiers.shift())),
                            Key::Named(Named::Enter | Named::Space)
                                if status == iced::event::Status::Ignored =>
                            {
                                Some(Message::Activate)
                            }
                            Key::Named(Named::PageDown)
                                if status == iced::event::Status::Ignored =>
                            {
                                Some(Message::Scroll(240.0))
                            }
                            Key::Named(Named::PageUp) if status == iced::event::Status::Ignored => {
                                Some(Message::Scroll(-240.0))
                            }
                            _ => None,
                        };
                    }
                    None
                }),
            ])
        })
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
