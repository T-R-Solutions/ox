use crate::design::{Appearance, ButtonRole, Density, EvidenceState};
use crate::local_task::Controller;
use crate::workbench::Surface;
use iced::{Element, Task, widget::button};
use std::{
    fmt::Write as _,
    path::PathBuf,
    sync::{
        Arc, Mutex,
        atomic::{AtomicBool, Ordering},
    },
};
pub type Result = iced::Result;
mod folder_picker;
mod icons;
mod identity;
mod project_store;
mod views;
#[expect(
    clippy::struct_excessive_bools,
    reason = "Independent transient UI toggles; domain state lives in Controller"
)]
struct Desktop {
    controller: Arc<Mutex<Controller>>,
    cancel: Arc<AtomicBool>,
    path: String,
    selected: bool,
    workspace_error: Option<String>,
    picker: Option<folder_picker::Request>,
    picker_serial: u64,
    picker_error: Option<String>,
    picker_parent: bool,
    manual_path: bool,
    project_name: String,
    project_parent: String,
    project_request: Option<Arc<AtomicBool>>,
    recent: Vec<PathBuf>,
    history_busy: bool,
    history_serial: u64,
    history_error: Option<String>,
    reset_confirmation: bool,
    result: bool,
    busy: bool,
    closing: bool,
    generation: u64,
    status: String,
    details: bool,
    focus: Option<usize>,
    validation_label: Option<String>,
    appearance: Appearance,
    density: Density,
    surface: Surface,
    navigation_open: bool,
    width: f32,
    command_open: bool,
    command: String,
    command_selection: usize,
    return_focus: Option<usize>,
    draft: String,
    graph_exploratory: bool,
    demo_document: usize,
    demo_tool: usize,
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
            workspace_error: None,
            picker: None,
            picker_serial: 0,
            picker_error: None,
            picker_parent: false,
            manual_path: false,
            project_name: String::new(),
            project_parent: String::new(),
            project_request: None,
            recent: Vec::new(),
            history_busy: false,
            history_serial: 0,
            history_error: None,
            reset_confirmation: false,
            result: false,
            busy: false,
            closing: false,
            generation: 0,
            status:
                "UNVERIFIED. Controlled fixture; no sandbox or remote agents. Task history is session-only."
                    .into(),
            details: false,
            focus: None,
            validation_label: std::env::var("OX_VALIDATION_SESSION").ok(),
            appearance: Appearance::default(),
            density: Density::default(),
            surface: Surface::default(),
            navigation_open: true,
            width: 1280.0,
            command_open: false,
            command: String::new(),
            command_selection: 0,
            return_focus: None,
            draft: String::new(),
            graph_exploratory: false,
            demo_document: 0,
            demo_tool: 0,
        }
    }
}
#[derive(Clone, Debug)]
enum Message {
    Path(String),
    Select,
    ChooseFolder,
    ManualPath,
    ProjectName(String),
    ProjectParent(String),
    CreateProject,
    OpenRecent(PathBuf),
    History(HistoryAction),
    ResetConfirmation(bool),
    HistoryDone(u64, std::result::Result<Vec<PathBuf>, String>),
    ProjectDone(u64, OpenOutcome),
    FolderChosen(u64, folder_picker::Selection),
    Start(&'static str),
    Verify,
    Refresh,
    Cancel,
    Close,
    Toggle,
    Focus(bool),
    Activate,
    InputFocused(usize),
    Scroll(f32),
    Navigate(Surface),
    Appearance(Appearance),
    CycleAppearance,
    Density(Density),
    CycleDensity,
    Navigation,
    Resize(f32),
    Command,
    CommandInput(String),
    CommandGo,
    CommandMove(bool),
    Escape,
    Draft(String),
    GraphMode(bool),
    DemoDocument(usize),
    DemoTool(usize),
    Done(u64, Action, std::result::Result<String, String>),
}
#[derive(Clone, Copy, Debug)]
enum Action {
    Start,
    Verify,
    Refresh,
}
#[derive(Clone, Debug)]
enum HistoryAction {
    Load,
    Remove(PathBuf),
    Reset,
}
#[derive(Clone, Debug)]
struct OpenOutcome {
    result: std::result::Result<String, String>,
    canonical: Option<PathBuf>,
    history: Option<std::result::Result<Vec<PathBuf>, String>>,
    created: Option<PathBuf>,
}

// Query the actual layout rather than estimating row heights. Full paths and
// diagnostics may wrap to arbitrary heights at the minimum window size.
struct RevealControl {
    target: iced::widget::Id,
    bounds: Option<iced::Rectangle>,
    viewport: Option<(iced::Rectangle, iced::Vector)>,
}
impl iced::advanced::widget::Operation<Message> for RevealControl {
    fn traverse(
        &mut self,
        operate: &mut dyn FnMut(&mut dyn iced::advanced::widget::Operation<Message>),
    ) {
        operate(self);
    }
    fn container(&mut self, id: Option<&iced::widget::Id>, bounds: iced::Rectangle) {
        if id == Some(&self.target) {
            self.bounds = Some(bounds);
        }
    }
    fn scrollable(
        &mut self,
        id: Option<&iced::widget::Id>,
        bounds: iced::Rectangle,
        _: iced::Rectangle,
        translation: iced::Vector,
        _: &mut dyn iced::advanced::widget::operation::Scrollable,
    ) {
        if id == Some(&iced::widget::Id::new("main")) {
            self.viewport = Some((bounds, translation));
        }
    }
    fn finish(&self) -> iced::advanced::widget::operation::Outcome<Message> {
        use iced::advanced::widget::operation::{Outcome, scrollable};
        if let (Some(target), Some((viewport, translation))) = (self.bounds, self.viewport) {
            let top = target.y - translation.y;
            let bottom = top + target.height;
            let delta = if top < viewport.y + 8.0 {
                top - viewport.y - 8.0
            } else if bottom > viewport.y + viewport.height - 8.0 {
                bottom - viewport.y - viewport.height + 8.0
            } else {
                0.0
            };
            if delta.abs() > 0.5 {
                return Outcome::Chain(Box::new(scrollable::scroll_by(
                    iced::widget::Id::new("main"),
                    scrollable::AbsoluteOffset { x: 0.0, y: delta },
                )));
            }
        }
        Outcome::None
    }
}
impl Desktop {
    const fn entry(&self) -> bool {
        matches!(self.surface, Surface::Start | Surface::NewProject)
    }
    const fn project_available(&self) -> bool {
        !self.busy && !self.history_busy && !self.closing && self.picker.is_none()
    }
    fn reveal(id: usize) -> Task<Message> {
        iced::advanced::widget::operate(RevealControl {
            target: iced::widget::Id::from(format!("welcome-control-{id}")),
            bounds: None,
            viewport: None,
        })
    }
    fn initialize() -> (Self, Task<Message>) {
        let mut state = Self::default();
        let task = state.history(HistoryAction::Load);
        (state, task)
    }
    fn history(&mut self, action: HistoryAction) -> Task<Message> {
        if self.history_busy || self.busy || self.closing || self.picker.is_some() {
            return Task::none();
        }
        self.history_busy = true;
        self.history_serial += 1;
        self.reset_confirmation = false;
        let id = self.history_serial;
        let (send, receive) = iced::futures::channel::oneshot::channel();
        let spawn = std::thread::Builder::new()
            .name("ox-recent-projects".into())
            .spawn(move || {
                let result = project_store::history_path().and_then(|p| {
                    let store = project_store::RecentStore::new(p);
                    match action {
                        HistoryAction::Load => store.load(),
                        HistoryAction::Remove(path) => store.remove(&path),
                        HistoryAction::Reset => store.reset(),
                    }
                });
                let _ = send.send(result);
            });
        if let Err(error) = spawn {
            self.history_busy = false;
            self.history_error = Some(format!("Histórico indisponível: {error}"));
            return Task::none();
        }
        Task::perform(
            async move {
                receive
                    .await
                    .unwrap_or_else(|_| Err("Worker de histórico terminou sem resposta".into()))
            },
            move |result| Message::HistoryDone(id, result),
        )
    }
    fn open_project(&mut self, create: bool) -> Task<Message> {
        if !self.project_available() {
            return Task::none();
        }
        if create && !std::path::Path::new(&self.project_parent).is_absolute() {
            self.workspace_error = Some("Informe o caminho absoluto da pasta de destino.".into());
            return Task::none();
        }
        self.busy = true;
        self.selected = false;
        self.result = false;
        self.generation += 1;
        let generation = self.generation;
        let flag = Arc::new(AtomicBool::new(false));
        self.project_request = Some(flag.clone());
        self.workspace_error = None;
        self.status = if create {
            "Criando a pasta vazia…"
        } else {
            "Validando o diretório do projeto…"
        }
        .into();
        let path = self.path.clone();
        let parent = self.project_parent.clone();
        let name = self.project_name.clone();
        let controller = self.controller.clone();
        let (send, receive) = iced::futures::channel::oneshot::channel();
        let spawn = std::thread::Builder::new()
            .name("ox-open-project".into())
            .spawn(move || {
                let mut outcome = OpenOutcome {
                    result: Err("Abertura cancelada".into()),
                    canonical: None,
                    history: None,
                    created: None,
                };
                let result = (|| {
                    if flag.load(Ordering::Relaxed) {
                        return Err("Abertura cancelada".into());
                    }
                    let path = if create {
                        let destination =
                            project_store::create_project(std::path::Path::new(&parent), &name)?;
                        outcome.created = Some(destination.clone());
                        destination
                    } else {
                        PathBuf::from(path)
                    };
                    if flag.load(Ordering::Relaxed) {
                        return Err("Abertura cancelada".into());
                    }
                    let path = path.canonicalize().map_err(|e| e.to_string())?;
                    if path.to_str().is_none() {
                        return Err("O caminho real não é UTF-8; escolha outra pasta".into());
                    }
                    let mut controller = controller
                        .lock()
                        .map_err(|_| "Estado do projeto indisponível".to_owned())?;
                    let status = controller.select(&path).map_err(|e| e.to_string())?;
                    let canonical = controller
                        .workspace
                        .clone()
                        .ok_or_else(|| "Diretório validado ausente".to_owned())?;
                    drop(controller);
                    outcome.history = Some(
                        project_store::history_path()
                            .and_then(|p| project_store::RecentStore::new(p).record(&canonical)),
                    );
                    outcome.canonical = Some(canonical);
                    Ok(status)
                })();
                outcome.result = result;
                let _ = send.send(outcome);
            });
        if let Err(error) = spawn {
            self.busy = false;
            self.project_request = None;
            self.workspace_error = Some(format!("Não foi possível iniciar a abertura: {error}"));
            return Task::none();
        }
        Task::perform(
            async move {
                receive.await.unwrap_or_else(|_| OpenOutcome {result: Err("Worker terminou sem resposta; confira o destino antes de tentar criar novamente".into()), canonical: None, history: None, created: None})
            },
            move |result| Message::ProjectDone(generation, result),
        )
    }
    // Visual/tab order. Iced 0.14 buttons do not implement native keyboard focus.
    fn controls(&self) -> Vec<(usize, Message)> {
        if self.command_open {
            let mut controls = vec![(300, Message::Activate), (301, Message::Escape)];
            controls.extend(
                self.command_matches()
                    .iter()
                    .map(|s| (s.id(), Message::Navigate(*s))),
            );
            return controls;
        }
        if self.entry() {
            return self.entry_controls();
        }
        let mut controls = vec![
            (212, Message::Navigation),
            (213, Message::Command),
            (210, Message::CycleAppearance),
            (211, Message::CycleDensity),
            (0, Message::Toggle),
            (1, Message::Close),
        ];
        if self.busy {
            controls.push((214, Message::Cancel));
        }
        if self.navigation_open {
            controls.extend(Surface::ALL.iter().map(|s| (s.id(), Message::Navigate(*s))));
        }
        let content_visible = !self.navigation_open || self.width >= 980.0;
        let workspace = content_visible
            && matches!(
                self.surface,
                Surface::Start | Surface::Project | Surface::Tasks
            );
        if self.project_available() && workspace {
            controls.push((2, Message::Activate));
            if self.surface == Surface::Start && self.picker.is_none() {
                controls.push((273, Message::ChooseFolder));
            }
            controls.push((3, Message::Select));
            if self.selected && self.surface == Surface::Tasks {
                controls.extend([
                    (4, Message::Start("good")),
                    (5, Message::Start("bad")),
                    (6, Message::Start("failure")),
                    (7, Message::Start("hang")),
                ]);
            }
            if self.result && self.surface == Surface::Tasks {
                controls.extend([(9, Message::Verify), (10, Message::Refresh)]);
            }
        }
        if self.busy && content_visible && self.surface == Surface::Tasks {
            controls.push((8, Message::Cancel));
        }
        if content_visible {
            match self.surface {
                Surface::Start => {
                    if self.selected && !self.closing {
                        controls.push((270, Message::Navigate(Surface::Tasks)));
                    }
                    controls.extend([
                        (271, Message::Navigate(Surface::Activity)),
                        (272, Message::Navigate(Surface::Appearance)),
                    ]);
                }
                Surface::Appearance | Surface::Settings => {
                    controls.extend(
                        Appearance::ALL
                            .iter()
                            .enumerate()
                            .map(|(i, a)| (220 + i, Message::Appearance(*a))),
                    );
                    controls.extend([
                        (223, Message::Density(Density::Comfortable)),
                        (224, Message::Density(Density::Compact)),
                    ]);
                }
                Surface::Editor | Surface::Focus => {
                    controls.extend((0..3).map(|i| (250 + i, Message::DemoDocument(i))));
                    controls.extend((0..3).map(|i| (253 + i, Message::DemoDocument(i))));
                    controls.extend((0..3).map(|i| (260 + i, Message::DemoTool(i))));
                }
                Surface::NewTask => controls.push((230, Message::Activate)),
                Surface::Architecture => controls.extend([
                    (240, Message::GraphMode(false)),
                    (241, Message::GraphMode(true)),
                ]),
                _ => {}
            }
        }
        controls
    }
    fn entry_controls(&self) -> Vec<(usize, Message)> {
        let mut controls = vec![(272, Message::Navigate(Surface::Settings))];
        if self.project_available() {
            if self.surface == Surface::NewProject {
                controls.extend([
                    (290, Message::Activate),
                    (291, Message::Activate),
                    (292, Message::ChooseFolder),
                    (293, Message::CreateProject),
                ]);
            } else {
                controls.extend([
                    (273, Message::ChooseFolder),
                    (274, Message::Navigate(Surface::NewProject)),
                ]);
                controls.push((275, Message::ManualPath));
                if self.manual_path {
                    controls.extend([(2, Message::Activate), (3, Message::Select)]);
                }
                if self.history_error.is_some() {
                    controls.extend([
                        (280, Message::History(HistoryAction::Load)),
                        (281, Message::ResetConfirmation(true)),
                    ]);
                    if self.reset_confirmation {
                        controls.extend([
                            (282, Message::History(HistoryAction::Reset)),
                            (283, Message::ResetConfirmation(false)),
                        ]);
                    }
                }
                for (i, path) in self.recent.iter().enumerate() {
                    controls.extend([
                        (400 + i * 2, Message::OpenRecent(path.clone())),
                        (
                            401 + i * 2,
                            Message::History(HistoryAction::Remove(path.clone())),
                        ),
                    ]);
                }
            }
        }
        if self.surface == Surface::NewProject && !self.busy && !self.closing {
            controls.push((294, Message::Navigate(Surface::Start)));
        }
        if self.surface == Surface::Start && self.selected && !self.closing {
            let position = controls
                .iter()
                .position(|(id, _)| *id == 275)
                .unwrap_or(controls.len());
            controls.insert(position, (270, Message::Navigate(Surface::Tasks)));
        }
        controls
    }
    fn control<'a>(
        &self,
        index: usize,
        label: &'a str,
        message: Option<Message>,
    ) -> iced::widget::Button<'a, Message> {
        self.styled_control(index, label, message, ButtonRole::Secondary)
    }
    fn styled_control<'a>(
        &self,
        index: usize,
        label: &'a str,
        message: Option<Message>,
        role: ButtonRole,
    ) -> iced::widget::Button<'a, Message> {
        let focused = self.focus == Some(index);
        let p = self.appearance.palette();
        let kind = match index {
            273 | 292 => Some(icons::Kind::Folder),
            274 => Some(icons::Kind::Plus),
            272 | 210 | 211 => Some(icons::Kind::Settings),
            212 => Some(icons::Kind::Panels),
            213 => Some(icons::Kind::Search),
            275 => Some(icons::Kind::File),
            270 => Some(icons::Kind::Activity),
            _ => None,
        };
        let mut content = iced::widget::row![]
            .spacing(8)
            .align_y(iced::Alignment::Center);
        if let Some(kind) = kind {
            content = content.push(icons::icon(kind));
        }
        content = content.push(iced::widget::text(label).size(14));
        button(content)
            .padding(self.density.control_padding())
            .on_press_maybe(message)
            .style(move |_, status| crate::design::button_style(p, role, focused, status))
    }
    fn command_matches(&self) -> Vec<Surface> {
        let query = self.command.trim().to_lowercase();
        Surface::ALL
            .iter()
            .copied()
            .filter(|s| {
                s.title().to_lowercase().contains(&query) || s.code().to_lowercase() == query
            })
            .collect()
    }
    fn restore_visible_focus(&mut self) {
        if self
            .focus
            .is_some_and(|id| !self.controls().iter().any(|(i, _)| *i == id))
        {
            self.focus = Some(if self.entry() { 272 } else { 212 });
        }
    }
    fn cancel_picker(&self) {
        if let Some(picker) = &self.picker {
            picker.cancel.store(true, Ordering::Relaxed);
        }
    }
    fn choose_folder(&mut self) -> Task<Message> {
        if !self.entry() || !self.project_available() {
            return Task::none();
        }
        self.picker_parent = self.surface == Surface::NewProject;
        self.picker_serial += 1;
        let id = self.picker_serial;
        let cancel = Arc::new(AtomicBool::new(false));
        let flag = cancel.clone();
        let (send, receive) = iced::futures::channel::oneshot::channel();
        let spawn = std::thread::Builder::new()
            .name("ox-folder-picker".into())
            .spawn(move || {
                let result = folder_picker::choose(&flag);
                let _ = send.send(result);
            });
        if let Err(error) = spawn {
            self.picker_error = Some(format!(
                "Não foi possível abrir o seletor: {error}. Digite o caminho manualmente."
            ));
            if !self.picker_parent {
                self.manual_path = true;
            }
            let id = if self.picker_parent { 291 } else { 2 };
            self.focus = Some(id);
            return Task::batch([
                iced::widget::operation::focus(if self.picker_parent {
                    "project-parent"
                } else {
                    "workspace"
                }),
                Self::reveal(id),
            ]);
        }
        self.picker = Some(folder_picker::Request {
            id,
            generation: self.generation,
            cancel,
        });
        // Opening/cancelling a dialog never modifies domain or draft state.
        Task::perform(
            async move {
                receive.await.unwrap_or_else(|_| {
                    Err("O seletor terminou sem uma resposta. Digite o caminho manualmente.".into())
                })
            },
            move |result| Message::FolderChosen(id, result),
        )
    }
    fn launch(&mut self, action: Action, mode: &'static str) -> Task<Message> {
        if self.busy || self.closing {
            return Task::none();
        }
        self.cancel_picker();
        self.busy = true;
        self.generation += 1;
        let generation = self.generation;
        self.cancel.store(false, Ordering::Relaxed);
        self.status = match action {
            Action::Start => "Em execução: tarefa controlada; prazo do subprocesso de 10 segundos. Cancelar solicita término observado.",
            Action::Verify => "Verificando a tentativa atual; prazo do subprocesso de 10 segundos…",
            Action::Refresh => "Observando os inputs atuais…",
        }.into();
        let controller = self.controller.clone();
        let cancel = self.cancel.clone();
        let (send, receive) = iced::futures::channel::oneshot::channel();
        let spawn = std::thread::Builder::new()
            .name("ox-local-task".into())
            .spawn(move || {
                let result = controller
                    .lock()
                    .map_err(|_| "Worker state unavailable".to_owned())
                    .and_then(|mut c| {
                        match action {
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
    #[expect(
        clippy::too_many_lines,
        reason = "Exhaustive UI message dispatch delegates domain work to Controller"
    )]
    fn update(&mut self, message: Message) -> Task<Message> {
        match message {
            Message::Navigate(surface) => {
                self.cancel_picker();
                if let Some(flag) = &self.project_request {
                    flag.store(true, Ordering::Relaxed);
                }
                if surface == Surface::NewProject {
                    self.workspace_error = None;
                    self.picker_error = None;
                }
                if surface == Surface::Start && self.surface == Surface::NewProject {
                    self.workspace_error = None;
                    self.picker_error = None;
                }

                self.surface = surface;
                if self.command_open {
                    self.command_open = false;
                    self.command.clear();
                    self.focus = Some(213);
                }
                if self.width < 980.0 || surface == Surface::Focus {
                    self.navigation_open = false;
                }
                if self.entry() {
                    self.focus = Some(if surface == Surface::NewProject {
                        290
                    } else {
                        273
                    });
                }
                self.restore_visible_focus();
                if surface == Surface::NewProject {
                    return Task::batch([
                        iced::widget::operation::focus("project-name"),
                        iced::widget::operation::snap_to(
                            "main",
                            iced::widget::scrollable::RelativeOffset::START,
                        ),
                    ]);
                }
                return iced::widget::operation::snap_to(
                    "main",
                    iced::widget::scrollable::RelativeOffset::START,
                );
            }
            Message::Appearance(appearance) => self.appearance = appearance,
            Message::CycleAppearance => self.appearance = self.appearance.next(),
            Message::Density(density) => self.density = density,
            Message::CycleDensity => self.density = self.density.next(),
            Message::Navigation => {
                self.cancel_picker();
                self.navigation_open = !self.navigation_open;
                self.restore_visible_focus();
            }
            Message::Resize(width) => {
                if width < 980.0 && self.width >= 980.0 {
                    self.navigation_open = false;
                }
                self.width = width;
                self.restore_visible_focus();
            }
            Message::Command => {
                self.cancel_picker();
                self.return_focus = self.focus;
                self.command_open = true;
                self.command.clear();
                self.command_selection = 0;
                self.focus = Some(300);
                return iced::widget::operation::focus("command");
            }
            Message::CommandInput(query) => {
                self.command = query;
                self.command_selection = 0;
            }
            Message::CommandGo => {
                if let Some(surface) = self.command_matches().get(self.command_selection).copied() {
                    return self.update(Message::Navigate(surface));
                }
            }
            Message::CommandMove(backwards) if self.command_open => {
                let count = self.command_matches().len();
                if count > 0 {
                    self.command_selection = if backwards {
                        (self.command_selection + count - 1) % count
                    } else {
                        (self.command_selection + 1) % count
                    };
                }
            }
            Message::Escape => {
                if self.command_open {
                    self.command_open = false;
                    self.focus = self.return_focus.take();
                    self.restore_visible_focus();
                } else if self.surface == Surface::NewProject && !self.busy {
                    return self.update(Message::Navigate(Surface::Start));
                }
            }
            Message::ManualPath if self.project_available() => {
                self.manual_path = !self.manual_path;
                if self.manual_path {
                    self.focus = Some(2);
                    return Task::batch([
                        iced::widget::operation::focus("workspace"),
                        Self::reveal(2),
                    ]);
                }
            }
            Message::ProjectName(name) if self.project_available() => {
                self.project_name = name;
                self.workspace_error = None;
                self.focus = Some(290);
            }
            Message::ProjectParent(parent) if !self.busy && !self.closing => {
                self.cancel_picker();
                self.project_parent = parent;
                self.workspace_error = None;
                self.focus = Some(291);
            }
            Message::CreateProject if self.surface == Surface::NewProject => {
                return self.open_project(true);
            }
            Message::OpenRecent(path)
                if self.project_available() && self.surface == Surface::Start =>
            {
                self.path = path.to_str().expect("history accepts only UTF-8").into();
                self.selected = false;
                self.result = false;
                return self.open_project(false);
            }
            Message::History(action) => return self.history(action),
            Message::ResetConfirmation(confirm) if !self.history_busy => {
                self.reset_confirmation = confirm;
            }
            Message::HistoryDone(id, result) if self.history_busy && id == self.history_serial => {
                self.history_busy = false;
                match result {
                    Ok(paths) => {
                        self.recent = paths;
                        self.history_error = None;
                    }
                    Err(error) => self.history_error = Some(error),
                }
                self.restore_visible_focus();
                if self.closing && !self.busy && self.picker.is_none() {
                    return iced::exit();
                }
            }
            Message::ProjectDone(id, outcome)
                if self.busy && id == self.generation && self.project_request.is_some() =>
            {
                self.busy = false;
                let canceled = self
                    .project_request
                    .take()
                    .expect("checked request")
                    .load(Ordering::Relaxed);
                if let Some(history) = outcome.history {
                    match history {
                        Ok(paths) => {
                            self.recent = paths;
                            self.history_error = None;
                        }
                        Err(error) => {
                            self.history_error = Some(format!(
                                "O projeto foi aberto, mas o histórico não foi salvo: {error}"
                            ));
                        }
                    }
                }
                self.selected = outcome.result.is_ok() && !canceled;
                if self.selected {
                    self.path = outcome
                        .canonical
                        .expect("successful open has canonical path")
                        .to_str()
                        .expect("canonical UTF-8 validated by store or selection")
                        .into();
                    self.surface = Surface::Tasks;
                    self.workspace_error = None;
                } else {
                    let mut error = outcome
                        .result
                        .as_ref()
                        .err()
                        .cloned()
                        .unwrap_or_else(|| "Abertura cancelada".into());
                    if let Some(created) = outcome.created {
                        let _ = write!(
                            error,
                            ". A pasta foi criada e preservada em {}. Abra-a como pasta existente; não repita a criação.",
                            created.display()
                        );
                    }
                    self.workspace_error = Some(error);
                }
                self.status = outcome
                    .result
                    .unwrap_or_else(|e| format!("UNVERIFIED — {e}"));
                self.restore_visible_focus();
                if self.closing && self.picker.is_none() && !self.history_busy {
                    return iced::exit();
                }
            }
            Message::Draft(draft) => self.draft = draft,
            Message::DemoDocument(index) if index < 3 => self.demo_document = index,
            Message::DemoTool(index) if index < 3 => self.demo_tool = index,
            Message::GraphMode(exploratory) => self.graph_exploratory = exploratory,
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
                let target = match self.focus {
                    Some(2) => "workspace",
                    Some(230) => "task-draft",
                    Some(300) => "command",
                    Some(290) => "project-name",
                    Some(291) => "project-parent",
                    _ => "no-text-input",
                };
                let focus = iced::widget::operation::focus(target);
                if self.entry() {
                    return Task::batch([focus, Self::reveal(controls[next].0)]);
                }
                if self.surface == Surface::Start
                    && self
                        .focus
                        .is_some_and(|id| matches!(id, 2 | 3 | 273 | 270..=272))
                {
                    return Task::batch([
                        focus,
                        iced::widget::operation::snap_to(
                            "main",
                            if self.focus.is_some_and(|id| (270..=272).contains(&id)) {
                                iced::widget::scrollable::RelativeOffset::END
                            } else {
                                iced::widget::scrollable::RelativeOffset::START
                            },
                        ),
                    ]);
                }
                if let Some(id) = self.focus.filter(|id| (100..127).contains(id)) {
                    return Task::batch([
                        focus,
                        iced::widget::operation::snap_to(
                            "navigation",
                            iced::widget::scrollable::RelativeOffset {
                                x: 0.0,
                                y: f32::from(
                                    u16::try_from(id - 100)
                                        .expect("navigation id bounded by Surface table"),
                                ) / 26.0,
                            },
                        ),
                    ]);
                }
                if self.focus.is_some_and(|id| (260..263).contains(&id)) {
                    return Task::batch([
                        focus,
                        iced::widget::operation::snap_to(
                            "main",
                            iced::widget::scrollable::RelativeOffset::END,
                        ),
                    ]);
                }
                return focus;
            }
            Message::InputFocused(id) => {
                // Mouse focus and explicit non-submitting Enter must agree with
                // the same traversal order used by keyboard button activation.
                if self.controls().iter().any(|(control, _)| *control == id) {
                    self.focus = Some(id);
                }
            }
            Message::Activate => {
                if let Some((_, action)) = self.controls().into_iter().find(|(id, _)| {
                    Some(*id) == self.focus && ![2, 230, 290, 291, 300].contains(id)
                }) {
                    return self.update(action);
                }
            }
            Message::Toggle => self.details = !self.details,
            Message::ChooseFolder => return self.choose_folder(),
            Message::FolderChosen(id, result) => {
                if self.picker.as_ref().is_none_or(|p| p.id != id) {
                    return Task::none();
                }
                let picker = self.picker.take().expect("matching request");
                let current = !picker.cancel.load(Ordering::Relaxed)
                    && picker.generation == self.generation
                    && self.surface
                        == if self.picker_parent {
                            Surface::NewProject
                        } else {
                            Surface::Start
                        }
                    && !self.busy
                    && !self.closing;
                if self.closing && !self.busy {
                    return iced::exit();
                }
                if !current {
                    return Task::none();
                }
                match result {
                    Ok(Some(path)) if self.picker_parent => {
                        self.project_parent = path;
                        self.focus = Some(293);
                        return Task::batch([
                            iced::widget::operation::focus("no-text-input"),
                            Self::reveal(293),
                        ]);
                    }
                    Ok(Some(path)) => {
                        let _ = self.update(Message::Path(path));
                        return self.update(Message::Select);
                    }
                    Ok(None) => {}
                    Err(error) => self.picker_error = Some(error),
                }
                let id = if self.picker_parent { 291 } else { 273 };
                self.focus = Some(id);
                return Task::batch([
                    iced::widget::operation::focus(if self.picker_parent {
                        "project-parent"
                    } else {
                        "no-text-input"
                    }),
                    Self::reveal(id),
                ]);
            }
            Message::Path(path) if !self.busy && !self.closing => {
                self.cancel_picker();
                self.picker_error = None;
                self.generation += 1;
                self.path = path;
                self.focus = Some(2);
                self.selected = false;
                self.workspace_error = None;
                self.result = false;
                self.status = "UNVERIFIED — valide o diretório do projeto".into();
            }
            Message::Select if self.project_available() => {
                self.cancel_picker();
                self.selected = false;
                self.workspace_error = None;
                self.result = false;
                return self.open_project(false);
            }
            Message::Start(mode) if self.selected && !self.busy => {
                self.result = false;
                return self.launch(Action::Start, mode);
            }
            Message::Verify if self.result => return self.launch(Action::Verify, ""),
            Message::Refresh if self.result => return self.launch(Action::Refresh, ""),
            Message::Cancel if self.busy => {
                self.cancel.store(true, Ordering::Relaxed);
                if let Some(flag) = &self.project_request {
                    flag.store(true, Ordering::Relaxed);
                }
                self.status =
                    "Cancelamento solicitado; aguardando o término observado do processo supervisionado."
                        .into();
            }
            Message::Close => {
                self.cancel_picker();
                self.closing = true;
                self.cancel.store(true, Ordering::Relaxed);
                if let Some(flag) = &self.project_request {
                    flag.store(true, Ordering::Relaxed);
                }
                if !self.busy && !self.history_busy && self.picker.is_none() {
                    return iced::exit();
                }
                self.status = "Encerrando: aguardando o término do trabalho supervisionado…".into();
            }
            Message::Done(g, action, result) if g == self.generation && self.busy => {
                self.busy = false;
                if matches!(action, Action::Start) {
                    self.result = result.is_ok();
                }
                self.status = result.unwrap_or_else(|e| format!("UNVERIFIED — {e}"));
                self.restore_visible_focus();
                if self.closing && self.picker.is_none() {
                    return iced::exit();
                }
            }
            _ => {}
        }
        Task::none()
    }
}
/// # Errors
/// Returns the Iced initialization or event-loop error when the native desktop cannot run.
pub fn run() -> Result {
    iced::application(Desktop::initialize, Desktop::update, Desktop::view)
        .title(|s: &Desktop| {
            let title = format!(
                "Ox — {} — {} — {}{}",
                s.surface.title(),
                s.appearance.label(),
                s.density.label(),
                if s.details { " • detalhes" } else { "" }
            );
            if let Some(label) = &s.validation_label {
                format!("{title} [{label}]")
            } else {
                title
            }
        })
        .window_size((1280.0, 820.0))
        .default_font(crate::design::UI_FONT)
        .font(include_bytes!("../assets/fonts/IBMPlexSans-Regular.ttf").as_slice())
        .font(include_bytes!("../assets/fonts/IBMPlexSans-SemiBold.ttf").as_slice())
        .font(include_bytes!("../assets/fonts/IBMPlexMono-Regular.ttf").as_slice())
        .theme(|s: &Desktop| s.appearance.theme())
        .exit_on_close_request(false)
        .subscription(|_| {
            iced::Subscription::batch([
                iced::window::close_requests().map(|_| Message::Close),
                iced::event::listen_with(|event, status, _| {
                    if let iced::Event::Window(iced::window::Event::Resized(size)) = &event {
                        return Some(Message::Resize(size.width));
                    }
                    if let iced::Event::Keyboard(iced::keyboard::Event::KeyPressed {
                        key,
                        modifiers,
                        ..
                    }) = event
                    {
                        use iced::keyboard::{Key, key::Named};
                        return match key {
                            Key::Character(ref ch)
                                if modifiers.control() && ch.eq_ignore_ascii_case("k") =>
                            {
                                Some(Message::Command)
                            }
                            Key::Named(Named::ArrowUp) => Some(Message::CommandMove(true)),
                            Key::Named(Named::ArrowDown) => Some(Message::CommandMove(false)),
                            Key::Named(Named::Escape) => Some(Message::Escape),
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
    fn pending_ui() -> Desktop {
        Desktop {
            picker: Some(folder_picker::Request {
                id: 5,
                generation: 8,
                cancel: Arc::new(AtomicBool::new(false)),
            }),
            picker_serial: 5,
            generation: 8,
            selected: true,
            result: true,
            path: "/original".into(),
            status: "prior verification".into(),
            workspace_error: Some("prior error".into()),
            navigation_open: false,
            ..Desktop::default()
        }
    }
    #[test]
    fn folder_cancel_preserves_workspace_evidence_and_rejects_duplicates() {
        let mut ui = pending_ui();
        let _ = ui.update(Message::ChooseFolder);
        assert_eq!(ui.picker_serial, 5);
        let _ = ui.update(Message::FolderChosen(4, Ok(Some("/late".into()))));
        assert!(ui.picker.is_some());
        let _ = ui.update(Message::FolderChosen(5, Ok(None)));
        assert!(ui.picker.is_none());
        assert_eq!(ui.path, "/original");
        assert!(ui.selected);
        assert!(ui.result);
        assert_eq!(ui.status, "prior verification");
        assert_eq!(ui.workspace_error.as_deref(), Some("prior error"));
        assert_eq!(ui.focus, Some(273));
        assert_eq!(ui.generation, 8);
    }
    #[test]
    fn folder_error_is_recoverable_without_mutating_prior_selection() {
        let mut ui = pending_ui();
        let _ = ui.update(Message::FolderChosen(5, Err("desktop unavailable".into())));
        assert_eq!(ui.picker_error.as_deref(), Some("desktop unavailable"));
        assert_eq!(ui.path, "/original");
        assert!(ui.selected);
        assert!(ui.result);
        assert_eq!(ui.status, "prior verification");
        let _ = ui.update(Message::Path("/manual".into()));
        assert!(ui.picker_error.is_none());
    }
    #[test]
    fn folder_late_results_after_edit_navigation_or_close_have_no_effect() {
        for action in [
            Message::Path("/edited".into()),
            Message::Navigate(Surface::Tasks),
            Message::Close,
        ] {
            let mut ui = pending_ui();
            let flag = ui.picker.as_ref().unwrap().cancel.clone();
            let _ = ui.update(action);
            assert!(flag.load(Ordering::Relaxed));
            let path = ui.path.clone();
            let selected = ui.selected;
            let _ = ui.update(Message::FolderChosen(5, Ok(Some("/late".into()))));
            assert!(ui.picker.is_none());
            assert!(!ui.busy);
            assert_eq!(ui.path, path);
            assert_eq!(ui.selected, selected);
        }
    }
    #[test]
    fn folder_confirmation_enters_validation_without_executing_task() {
        let mut ui = pending_ui();
        let _ = ui.update(Message::FolderChosen(
            5,
            Ok(Some("/not-an-existing-folder-for-ox".into())),
        ));
        assert_eq!(ui.path, "/not-an-existing-folder-for-ox");
        assert!(ui.busy);
        assert!(!ui.result);
        assert!(!ui.selected);
        assert_eq!(ui.surface, Surface::Start);
        assert!(ui.status.contains("Validando"));
    }
    #[test]
    fn parent_picker_only_edits_the_creation_destination_and_never_creates() {
        let mut ui = pending_ui();
        ui.surface = Surface::NewProject;
        ui.picker_parent = true;
        let _ = ui.update(Message::FolderChosen(5, Ok(Some("/chosen-parent".into()))));
        assert_eq!(ui.project_parent, "/chosen-parent");
        assert_eq!(ui.path, "/original");
        assert!(ui.selected);
        assert!(ui.result);
        assert!(!ui.busy);
        assert!(ui.project_request.is_none());
        assert_eq!(ui.focus, Some(293));
        assert_eq!(ui.controller.lock().unwrap().attempt, 0);
    }
    #[test]
    fn folder_controls_match_visibility_busy_and_keyboard_order() {
        let mut ui = Desktop {
            navigation_open: false,
            ..Desktop::default()
        };
        let ids: Vec<_> = ui.controls().into_iter().map(|(id, _)| id).collect();
        assert_eq!(&ids[..4], &[272, 273, 274, 275]);
        assert!(!ids.contains(&2));
        let _ = ui.update(Message::ManualPath);
        let ids: Vec<_> = ui.controls().into_iter().map(|(id, _)| id).collect();
        let input = ids.iter().position(|id| *id == 2).unwrap();
        assert_eq!(&ids[input..input + 2], &[2, 3]);
        ui.busy = true;
        assert!(!ui.controls().iter().any(|(id, _)| *id == 273));
        let _ = ui.update(Message::ChooseFolder);
        assert!(ui.picker.is_none());
        ui.busy = false;
        ui.closing = true;
        let _ = ui.update(Message::ChooseFolder);
        assert!(ui.picker.is_none());
    }
    #[test]
    fn start_resume_is_available_only_for_a_validated_visible_session() {
        let mut ui = Desktop {
            surface: Surface::Start,
            navigation_open: false,
            ..Desktop::default()
        };
        assert!(!ui.controls().iter().any(|(id, _)| *id == 270));
        assert!(ui.controls().iter().any(|(id, _)| *id == 272));
        ui.selected = true;
        ui.busy = true;
        ui.generation = 7;
        ui.focus = Some(270);
        let _ = ui.update(Message::Activate);
        assert_eq!(ui.surface, Surface::Tasks);
        assert!(ui.busy);
        assert!(ui.selected);
        assert_eq!(ui.generation, 7);
        assert!(!ui.cancel.load(Ordering::Relaxed));
        let _ = ui.update(Message::Navigate(Surface::Start));
        let _ = ui.update(Message::Resize(640.0));
        let _ = ui.update(Message::Navigation);
        assert!(ui.controls().iter().any(|(id, _)| *id == 270));
        let _ = ui.update(Message::Navigation);
        ui.busy = false;
        let _ = ui.update(Message::Path("/different".into()));
        assert!(!ui.selected);
        assert!(!ui.controls().iter().any(|(id, _)| *id == 270));
        assert_eq!(ui.focus, Some(2));
    }

    #[test]
    fn failed_workspace_selection_stays_at_entry_with_recoverable_error() {
        let mut ui = opening_ui();
        let _ = ui.update(Message::ProjectDone(
            9,
            OpenOutcome {
                result: Err("missing directory".into()),
                canonical: None,
                history: None,
                created: None,
            },
        ));
        assert_eq!(ui.surface, Surface::Start);
        assert!(!ui.selected);
        assert!(!ui.busy);
        assert_eq!(ui.workspace_error.as_deref(), Some("missing directory"));
        let _ = ui.update(Message::Path("/corrected".into()));
        assert!(ui.workspace_error.is_none());
        assert!(!ui.selected);
    }

    fn opening_ui() -> Desktop {
        Desktop {
            busy: true,
            generation: 9,
            project_request: Some(Arc::new(AtomicBool::new(false))),
            ..Desktop::default()
        }
    }
    fn opened(history: std::result::Result<Vec<PathBuf>, String>) -> OpenOutcome {
        OpenOutcome {
            result: Ok("Workspace selected".into()),
            canonical: Some(PathBuf::from("/canonical/project")),
            history: Some(history),
            created: None,
        }
    }
    #[test]
    fn history_load_serializes_project_actions_and_rejects_old_completions() {
        let mut ui = Desktop {
            history_busy: true,
            history_serial: 3,
            ..Desktop::default()
        };
        let _ = ui.update(Message::Select);
        let _ = ui.update(Message::CreateProject);
        let _ = ui.update(Message::History(HistoryAction::Remove(PathBuf::from(
            "/saved",
        ))));
        assert!(!ui.busy);
        assert!(ui.history_busy);
        assert_eq!(ui.history_serial, 3);
        let _ = ui.update(Message::HistoryDone(2, Ok(vec![PathBuf::from("/old")])));
        assert_eq!(ui.recent, Vec::<PathBuf>::new());
        assert!(ui.history_busy);
        let _ = ui.update(Message::HistoryDone(3, Ok(vec![PathBuf::from("/saved")])));
        assert!(!ui.history_busy);
        assert_eq!(ui.recent, vec![PathBuf::from("/saved")]);
        let _ = ui.update(Message::HistoryDone(3, Ok(vec![])));
        assert_eq!(ui.recent.len(), 1);
    }
    #[test]
    fn successful_open_survives_history_failure_without_starting_a_task() {
        let mut ui = opening_ui();
        let _ = ui.update(Message::ProjectDone(
            9,
            opened(Err("read only store".into())),
        ));
        assert_eq!(ui.surface, Surface::Tasks);
        assert_eq!(ui.path, "/canonical/project");
        assert!(ui.selected);
        assert!(!ui.busy);
        assert!(
            ui.history_error
                .as_ref()
                .unwrap()
                .contains("read only store")
        );
        assert!(ui.workspace_error.is_none());
        assert_eq!(ui.controller.lock().unwrap().attempt, 0);
        let _ = ui.update(Message::ProjectDone(9, opened(Ok(vec![]))));
        assert!(ui.history_error.is_some());
    }
    #[test]
    fn navigating_during_open_prevents_a_late_automatic_navigation() {
        let mut ui = opening_ui();
        let flag = ui.project_request.as_ref().unwrap().clone();
        let _ = ui.update(Message::Navigate(Surface::Settings));
        assert!(flag.load(Ordering::Relaxed));
        let _ = ui.update(Message::ProjectDone(
            9,
            opened(Ok(vec![PathBuf::from("/canonical/project")])),
        ));
        assert_eq!(ui.surface, Surface::Settings);
        assert!(!ui.selected);
        assert!(!ui.busy);
        assert_eq!(ui.controller.lock().unwrap().attempt, 0);
    }
    #[test]
    fn creation_requires_confirmation_and_reports_preserved_destination_on_failure() {
        let mut ui = Desktop::default();
        let _ = ui.update(Message::Navigate(Surface::NewProject));
        let _ = ui.update(Message::ProjectName("new-project".into()));
        let _ = ui.update(Message::ProjectParent("/some/parent".into()));
        assert!(!ui.busy);
        assert!(ui.project_request.is_none());
        let _ = ui.update(Message::Escape);
        assert_eq!(ui.surface, Surface::Start);
        assert!(!ui.busy);
        ui = opening_ui();
        ui.surface = Surface::NewProject;
        let _ = ui.update(Message::ProjectDone(
            9,
            OpenOutcome {
                result: Err("directory unavailable after creation".into()),
                canonical: None,
                history: None,
                created: Some(PathBuf::from("/parent/created")),
            },
        ));
        assert_eq!(ui.surface, Surface::NewProject);
        assert!(!ui.selected);
        let error = ui.workspace_error.as_ref().unwrap();
        assert!(error.contains("/parent/created"));
        assert!(error.contains("preservada"));
    }
    #[test]
    fn recent_controls_follow_each_item_and_creation_has_no_implicit_submit() {
        let mut ui = Desktop {
            recent: (0..20)
                .map(|i| PathBuf::from(format!("/project-{i}")))
                .collect(),
            width: 640.0,
            ..Desktop::default()
        };
        let ids: Vec<_> = ui.controls().into_iter().map(|(id, _)| id).collect();
        assert_eq!(&ids[ids.len() - 4..], &[436, 437, 438, 439]);
        ui.focus = Some(438);
        let _ = ui.update(Message::Focus(false));
        assert_eq!(ui.focus, Some(439));
        let _ = ui.update(Message::Focus(true));
        assert_eq!(ui.focus, Some(438));
        let _ = ui.update(Message::Navigate(Surface::NewProject));
        let ids: Vec<_> = ui.controls().into_iter().map(|(id, _)| id).collect();
        assert_eq!(ids, vec![272, 290, 291, 292, 293, 294]);
        assert_eq!(ui.focus, Some(290));
        let _ = ui.update(Message::Activate);
        assert!(!ui.busy);
    }
    #[test]
    fn reveal_uses_the_focused_controls_actual_bounds_including_scroll_translation() {
        use iced::advanced::widget::{
            Operation,
            operation::{
                Outcome, Scrollable,
                scrollable::{AbsoluteOffset, RelativeOffset},
            },
        };
        #[derive(Default)]
        struct DummyScroll;
        impl Scrollable for DummyScroll {
            fn snap_to(&mut self, _: RelativeOffset<Option<f32>>) {}
            fn scroll_to(&mut self, _: AbsoluteOffset<Option<f32>>) {}
            fn scroll_by(&mut self, _: AbsoluteOffset, _: iced::Rectangle, _: iced::Rectangle) {}
        }
        let mut reveal = RevealControl {
            target: iced::widget::Id::new("welcome-control-438"),
            bounds: None,
            viewport: None,
        };
        reveal.container(
            Some(&iced::widget::Id::new("welcome-control-438")),
            iced::Rectangle {
                x: 20.0,
                y: 2400.0,
                width: 400.0,
                height: 40.0,
            },
        );
        reveal.scrollable(
            Some(&iced::widget::Id::new("main")),
            iced::Rectangle {
                x: 0.0,
                y: 60.0,
                width: 640.0,
                height: 360.0,
            },
            iced::Rectangle::default(),
            iced::Vector::new(0.0, 2300.0),
            &mut DummyScroll,
        );
        assert!(matches!(reveal.finish(), Outcome::None));
        reveal.bounds.as_mut().unwrap().y = 2800.0;
        assert!(matches!(reveal.finish(), Outcome::Chain(_)));
        reveal.bounds.as_mut().unwrap().y = 2300.0;
        assert!(matches!(reveal.finish(), Outcome::Chain(_)));
    }

    #[test]
    fn captured_input_click_replaces_stale_button_focus_and_enter_never_confirms_creation() {
        let cases = [
            (
                Surface::NewProject,
                false,
                false,
                "project-name",
                290,
                291,
                true,
            ),
            (
                Surface::NewProject,
                false,
                false,
                "project-parent",
                291,
                292,
                true,
            ),
            (Surface::NewTask, false, false, "task-draft", 230, 212, true),
            (Surface::Tasks, false, false, "workspace", 2, 3, false),
            (Surface::Start, true, false, "workspace", 2, 3, false),
            (Surface::Start, false, true, "command", 300, 301, false),
        ];
        for (surface, manual_path, command_open, native_id, id, next, non_submitting) in cases {
            let mut ui = Desktop {
                surface,
                manual_path,
                command_open,
                focus: Some(293),
                project_name: "must-not-create".into(),
                project_parent: "/tmp".into(),
                ..Desktop::default()
            };
            exercise_input_click(&mut ui, native_id, id, next, non_submitting);
        }
    }

    struct Bounds {
        target: iced::widget::Id,
        found: Option<iced::Rectangle>,
    }
    impl iced::advanced::widget::Operation for Bounds {
        fn traverse(
            &mut self,
            operate: &mut dyn FnMut(&mut dyn iced::advanced::widget::Operation),
        ) {
            operate(self);
        }
        fn focusable(
            &mut self,
            id: Option<&iced::widget::Id>,
            bounds: iced::Rectangle,
            _: &mut dyn iced::advanced::widget::operation::Focusable,
        ) {
            if id == Some(&self.target) {
                self.found = Some(bounds);
            }
        }
    }
    #[test]
    fn welcome_chrome_preserves_work_area_at_desktop_sizes() {
        use iced::advanced::{layout, widget::Tree};
        let renderer = iced::Renderer::new(crate::design::UI_FONT, iced::Pixels(16.0));
        for (width, height) in [(640.0, 480.0), (1440.0, 900.0), (2560.0, 1080.0)] {
            let ui = Desktop {
                width,
                ..Desktop::default()
            };
            let mut element = ui.view();
            let mut tree = Tree::new(element.as_widget());
            let node = element.as_widget_mut().layout(
                &mut tree,
                &renderer,
                &layout::Limits::new(iced::Size::ZERO, iced::Size::new(width, height)),
            );
            let regions = node.children()[0].children();
            assert!(
                regions[0].bounds().height <= 60.0,
                "chrome consumes work area at {width}"
            );
            assert!(
                regions[1].bounds().height >= height - 100.0,
                "project area compressed at {width}"
            );
        }
    }
    fn exercise_input_click(
        ui: &mut Desktop,
        native_id: &'static str,
        id: usize,
        next: usize,
        non_submitting: bool,
    ) {
        use iced::advanced::{Layout, Shell, layout, widget::Tree};
        let mut element = ui.view();
        let mut tree = Tree::new(element.as_widget());
        let renderer = iced::Renderer::new(crate::design::UI_FONT, iced::Pixels(16.0));
        let viewport = iced::Rectangle {
            x: 0.0,
            y: 0.0,
            width: 1280.0,
            height: 820.0,
        };
        let node = element.as_widget_mut().layout(
            &mut tree,
            &renderer,
            &layout::Limits::new(iced::Size::ZERO, viewport.size()),
        );
        let layout = Layout::new(&node);
        let mut bounds = Bounds {
            target: iced::widget::Id::new(native_id),
            found: None,
        };
        element
            .as_widget_mut()
            .operate(&mut tree, layout, &renderer, &mut bounds);
        let cursor =
            iced::mouse::Cursor::Available(bounds.found.expect("visible native input").center());
        let mut click_messages = Vec::new();
        let mut shell = Shell::new(&mut click_messages);
        element.as_widget_mut().update(
            &mut tree,
            &iced::Event::Mouse(iced::mouse::Event::ButtonPressed(iced::mouse::Button::Left)),
            layout,
            cursor,
            &renderer,
            &mut iced::advanced::clipboard::Null,
            &mut shell,
            &viewport,
        );
        assert!(
            shell.is_event_captured(),
            "input must capture click: {native_id}"
        );
        assert!(
            click_messages
                .iter()
                .any(|m| matches!(m, Message::InputFocused(focused) if *focused == id)),
            "captured click must synchronize focus: {native_id}"
        );
        let mut submit_messages = Vec::new();
        if non_submitting {
            let event = enter_key_event();
            let mut shell = Shell::new(&mut submit_messages);
            element.as_widget_mut().update(
                &mut tree,
                &event,
                layout,
                cursor,
                &renderer,
                &mut iced::advanced::clipboard::Null,
                &mut shell,
                &viewport,
            );
            assert!(
                shell.is_event_captured(),
                "Enter must not reach global button activation: {native_id}"
            );
            assert!(
                submit_messages
                    .iter()
                    .all(|m| matches!(m, Message::InputFocused(focused) if *focused == id))
            );
        }
        drop(element);
        for message in click_messages {
            let _ = ui.update(message);
        }
        assert_eq!(ui.focus, Some(id));
        for message in submit_messages {
            let _ = ui.update(message);
        }
        assert!(!ui.busy);
        assert!(!ui.closing);
        assert!(ui.project_request.is_none());
        assert_eq!(ui.controller.lock().unwrap().attempt, 0);
        assert_eq!(ui.project_name, "must-not-create");
        assert_eq!(ui.project_parent, "/tmp");
        let _ = ui.update(Message::Focus(false));
        assert_eq!(
            ui.focus,
            Some(next),
            "Tab starts at actual clicked input: {native_id}"
        );
    }

    fn enter_key_event() -> iced::Event {
        let key = iced::keyboard::Key::Named(iced::keyboard::key::Named::Enter);
        iced::Event::Keyboard(iced::keyboard::Event::KeyPressed {
            key: key.clone(),
            modified_key: key,
            physical_key: iced::keyboard::key::Physical::Unidentified(
                iced::keyboard::key::NativeCode::Unidentified,
            ),
            location: iced::keyboard::Location::Standard,
            modifiers: iced::keyboard::Modifiers::empty(),
            text: None,
            repeat: false,
        })
    }

    #[test]
    fn demo_selection_is_bounded_and_has_no_domain_effect() {
        let mut ui = Desktop {
            surface: Surface::Editor,
            selected: true,
            generation: 7,
            ..Desktop::default()
        };
        let _ = ui.update(Message::DemoDocument(1));
        let _ = ui.update(Message::DemoTool(2));
        assert_eq!((ui.demo_document, ui.demo_tool), (1, 2));
        let _ = ui.update(Message::DemoDocument(99));
        let _ = ui.update(Message::DemoTool(99));
        assert_eq!((ui.demo_document, ui.demo_tool), (1, 2));
        assert!(ui.selected);
        assert_eq!(ui.generation, 7);
        assert!(!ui.busy);
        assert!(ui.controls().iter().any(|(id, _)| *id == 251));
        let _ = ui.update(Message::Navigate(Surface::Tasks));
        assert!(!ui.controls().iter().any(|(id, _)| *id == 251));
        assert_eq!(ui.demo_document, 1);
    }

    #[test]
    fn hidden_controls_and_modal_focus_preserve_domain_state() {
        let mut ui = Desktop {
            width: 800.0,
            surface: Surface::Tasks,
            navigation_open: true,
            busy: true,
            ..Desktop::default()
        };
        assert!(!ui.controls().iter().any(|(id, _)| *id == 2));
        assert!(ui.controls().iter().any(|(id, _)| *id == 214));
        ui.focus = Some(211);
        let _ = ui.update(Message::Command);
        assert!(
            ui.controls()
                .iter()
                .all(|(_, m)| !matches!(m, Message::Start(_) | Message::Cancel))
        );
        let _ = ui.update(Message::Escape);
        assert_eq!(ui.focus, Some(211));
        assert!(ui.busy);
        let _ = ui.update(Message::Navigate(Surface::Observability));
        assert!(ui.busy);
        assert!(!ui.cancel.load(Ordering::Relaxed));
        let _ = ui.update(Message::Activate);
        assert!(ui.busy);
    }

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
        let _ = ui.update(Message::Done(3, Action::Start, Ok("old".into())));
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
        let _ = ui.update(Message::Done(4, Action::Start, Ok("duplicate".into())));
        assert_ne!(ui.status, "duplicate");
        ui.closing = false;
        let _ = ui.update(Message::Path("/new".into()));
        let _ = ui.update(Message::Done(4, Action::Start, Ok("late workspace".into())));
        assert!(!ui.selected);
        assert_eq!(ui.path, "/new");
    }
}
