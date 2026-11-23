//! Workbench command chrome: title/command bar, command menus, status bar and
//! window title. Presentation only; every menu item dispatches an existing
//! `Message`, so menus never introduce new domain effects.
use super::{Desktop, Message, icons};
use crate::design::{self, ButtonRole, HEADING_FONT};
use crate::workbench::Surface;
use iced::widget::{Space, button, column, container, mouse_area, row, rule, space, stack, text};
use iced::{Alignment, Element, Length, Task};

/// Logical geometry shared by the bar and the dropdown placement. Menu
/// triggers have fixed widths so a dropdown can anchor without measuring.
const BAR_HEIGHT: f32 = 48.0;
const MENU_WIDTH: f32 = 84.0;
const MENU_GAP: f32 = 2.0;
/// Left padding 12 + panel toggle 32 + gap 6 + signature 128 + gap 6.
const MENU_X: f32 = 184.0;
const DROPDOWN_WIDTH: f32 = 320.0;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(super) enum Menu {
    File,
    View,
    Tools,
}
impl Menu {
    pub(super) const ALL: [Self; 3] = [Self::File, Self::View, Self::Tools];
    pub(super) const fn id(self) -> usize {
        match self {
            Self::File => 600,
            Self::View => 601,
            Self::Tools => 602,
        }
    }
    pub(super) const fn label(self) -> &'static str {
        match self {
            Self::File => "Arquivo",
            Self::View => "Exibir",
            Self::Tools => "Ferramentas",
        }
    }
    /// Left edge of the dropdown, aligned with the fixed-width trigger.
    const fn anchor(self) -> f32 {
        const STEP: f32 = MENU_WIDTH + MENU_GAP;
        match self {
            Self::File => MENU_X,
            Self::View => MENU_X + STEP,
            Self::Tools => MENU_X + STEP + STEP,
        }
    }
}

pub(super) struct MenuItem {
    pub(super) id: usize,
    pub(super) label: &'static str,
    /// Shortcut or current state, shown right-aligned.
    pub(super) detail: String,
    /// `None` renders a disabled item that is excluded from traversal.
    pub(super) action: Option<Message>,
    pub(super) separator: bool,
}
fn item(id: usize, label: &'static str, detail: &str, action: Option<Message>) -> MenuItem {
    MenuItem {
        id,
        label,
        detail: detail.into(),
        action,
        separator: false,
    }
}
const fn separated(mut entry: MenuItem) -> MenuItem {
    entry.separator = true;
    entry
}

impl Desktop {
    pub(super) fn menu_items(&self, menu: Menu) -> Vec<MenuItem> {
        match menu {
            Menu::File => vec![
                item(
                    610,
                    "Central de projetos",
                    "",
                    Some(Message::Navigate(Surface::Start)),
                ),
                item(
                    611,
                    "Novo projeto",
                    "",
                    Some(Message::Navigate(Surface::NewProject)),
                ),
                item(
                    612,
                    "Abrir pasta…",
                    "",
                    self.project_available().then_some(Message::OpenFolder),
                ),
                separated(item(613, "Sair", "", Some(Message::Close))),
            ],
            Menu::View => vec![
                item(620, "Navegação", "Ctrl+B", Some(Message::Navigation)),
                item(621, "Painel de ferramentas", "Ctrl+J", Some(Message::Dock)),
                item(
                    622,
                    "Reduzir navegação",
                    "Ctrl+Alt+←",
                    Some(Message::SidebarAdjust(-24.0)),
                ),
                item(
                    623,
                    "Ampliar navegação",
                    "Ctrl+Alt+→",
                    Some(Message::SidebarAdjust(24.0)),
                ),
                separated(item(
                    624,
                    "Alternar tema",
                    self.appearance.label(),
                    Some(Message::CycleAppearance),
                )),
                item(
                    625,
                    "Alternar densidade",
                    self.density.label(),
                    Some(Message::CycleDensity),
                ),
                item(
                    626,
                    "Limites da execução",
                    if self.details { "Exibidos" } else { "Ocultos" },
                    Some(Message::Toggle),
                ),
                separated(item(627, "Ir para…", "Ctrl+K", Some(Message::Command))),
            ],
            Menu::Tools => vec![
                item(
                    630,
                    "Ferramentas e plugins",
                    "",
                    Some(Message::Navigate(Surface::Tools)),
                ),
                separated(item(
                    631,
                    "Problemas",
                    "",
                    Some(Message::Navigate(Surface::Problems)),
                )),
                item(632, "Testes", "", Some(Message::Navigate(Surface::Tests))),
                item(
                    633,
                    "Rastro de execução",
                    "",
                    Some(Message::Navigate(Surface::Trace)),
                ),
                item(
                    634,
                    "Terminal",
                    "",
                    Some(Message::Navigate(Surface::Terminal)),
                ),
                separated(item(
                    635,
                    "Preferências",
                    "",
                    Some(Message::Navigate(Surface::Settings)),
                )),
            ],
        }
    }
    /// Opens a menu (focusing its first available item), toggles the same
    /// menu closed, or closes with `None`, returning focus to its trigger.
    pub(super) fn toggle_menu(&mut self, menu: Option<Menu>) -> Task<Message> {
        match menu {
            Some(menu) if self.menu != Some(menu) => {
                if self.command_open || self.entry() {
                    return Task::none();
                }
                self.navigation_drag = false;
                self.cancel_picker();
                self.menu = Some(menu);
                self.focus = self
                    .menu_items(menu)
                    .into_iter()
                    .find(|item| item.action.is_some())
                    .map(|item| item.id);
            }
            _ => {
                if let Some(open) = self.menu.take() {
                    self.focus = Some(open.id());
                }
            }
        }
        Task::none()
    }
    pub(super) fn run_menu_item(&mut self, id: usize) -> Task<Message> {
        let Some(menu) = self.menu else {
            return Task::none();
        };
        let Some(action) = self
            .menu_items(menu)
            .into_iter()
            .find(|item| item.id == id)
            .and_then(|item| item.action)
        else {
            return Task::none();
        };
        self.menu = None;
        self.focus = Some(menu.id());
        self.update(action)
    }
    pub(super) fn project_label(&self) -> Option<&str> {
        if !self.selected {
            return None;
        }
        std::path::Path::new(&self.path)
            .file_name()
            .and_then(|name| name.to_str())
    }
    /// Window title names the place and project; presentation preferences
    /// (theme, density, details) are not identity and stay out of it.
    pub(super) fn window_title(&self) -> String {
        let place = match self.surface {
            Surface::Start => "Central de projetos",
            Surface::NewProject => "Novo projeto",
            Surface::Settings | Surface::Appearance => "Preferências",
            surface => surface.title(),
        };
        let mut title = match self.project_label() {
            Some(project) if !self.entry() => format!("{place} — {project} — Ox"),
            _ => format!("{place} — Ox"),
        };
        if let Some(label) = &self.validation_label {
            title = format!("{title} [{label}]");
        }
        title
    }
    fn menu_trigger(&self, menu: Menu) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let focused = self.focus == Some(menu.id());
        let open = self.menu == Some(menu);
        button(text(menu.label()).size(14))
            .width(MENU_WIDTH)
            .padding([7, 10])
            .on_press(Message::Menu(Some(menu)))
            .style(move |_, status| {
                let mut style = design::button_style(p, ButtonRole::Chrome, focused, status);
                if open {
                    style.background = Some(p.shell_deep.into());
                }
                style
            })
            .into()
    }
    fn search_trigger(&self) -> Element<'_, Message> {
        if self.width < 1180.0 {
            return self.icon_control(
                213,
                "Ir para… · Ctrl+K",
                icons::Kind::Search,
                Message::Command,
            );
        }
        let p = self.appearance.palette();
        let focused = self.focus == Some(213);
        let control = button(
            row![
                icons::icon(icons::Kind::Search),
                text("Ir para uma tela…").size(13),
                space::horizontal(),
                text("Ctrl+K").size(12),
            ]
            .spacing(8)
            .align_y(Alignment::Center),
        )
        .width(320)
        .padding([7, 12])
        .on_press(Message::Command)
        .style(move |_, status| {
            let mut style = design::button_style(p, ButtonRole::Chrome, focused, status);
            style.background = Some(p.shell_deep.into());
            if !focused && matches!(status, button::Status::Hovered) {
                style.border.color = p.text_shell;
            }
            style
        });
        super::hint::focus(
            control.into(),
            container(text("Ir para… · Ctrl+K").size(13))
                .padding(8)
                .style(move |_| design::panel(p.surface_base, p.text_primary, p.border_interactive))
                .into(),
            focused,
        )
    }
    fn project_chip(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let focused = self.focus == Some(603);
        let mut content = row![icons::icon(icons::Kind::Folder)]
            .spacing(8)
            .align_y(Alignment::Center);
        if self.width >= 900.0 {
            content = content.push(
                text(self.project_label().unwrap_or("Nenhum projeto"))
                    .size(13)
                    .wrapping(text::Wrapping::None),
            );
        }
        content = content.push(icons::icon(icons::Kind::Chevron));
        let control = button(content)
            .padding([7, 10])
            .on_press(Message::Navigate(Surface::Start))
            .style(move |_, status| design::button_style(p, ButtonRole::Chrome, focused, status));
        let label = if self.selected {
            self.path.as_str()
        } else {
            "Nenhum projeto aberto · abrir a Central de projetos"
        };
        iced::widget::tooltip(
            control,
            container(text(label).size(13)).padding(8).style(move |_| {
                design::panel(p.surface_base, p.text_primary, p.border_interactive)
            }),
            iced::widget::tooltip::Position::Bottom,
        )
        .gap(6)
        .into()
    }
    /// 48-unit command bar: panels, OX signature, menus, centered go-to,
    /// project selector, tool dock and settings.
    pub(super) fn chrome_bar(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let menus = Menu::ALL
            .iter()
            .fold(row![].spacing(MENU_GAP), |menus, menu| {
                menus.push(self.menu_trigger(*menu))
            });
        container(
            row![
                self.icon_control(
                    212,
                    "Recolher / expandir navegação · Ctrl+B",
                    icons::Kind::Panels,
                    Message::Navigation
                ),
                iced::widget::image(super::identity::signature(
                    self.appearance == crate::design::Appearance::HighContrast
                ))
                .width(128)
                .height(40)
                .content_fit(iced::ContentFit::Contain),
                menus,
                space::horizontal(),
                self.search_trigger(),
                space::horizontal(),
                self.project_chip(),
                self.icon_control(
                    644,
                    "Painel de ferramentas · Ctrl+J",
                    icons::Kind::Dock,
                    Message::Dock
                ),
                self.icon_control(
                    272,
                    "Configurações",
                    icons::Kind::Settings,
                    Message::Navigate(Surface::Settings)
                ),
            ]
            .spacing(6)
            .align_y(Alignment::Center),
        )
        .padding([4, 12])
        .height(BAR_HEIGHT)
        .width(Length::Fill)
        .style(move |_| container::Style {
            background: Some(p.shell_bg.into()),
            text_color: Some(p.text_shell),
            ..Default::default()
        })
        .into()
    }
    /// Dropdown anchored under its trigger. A transparent backdrop consumes
    /// the dismissing click so it never activates an underlying control.
    pub(super) fn menu_overlay(&self, menu: Menu) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mut list = column![].spacing(0);
        for entry in self.menu_items(menu) {
            if entry.separator {
                list = list.push(container(rule::horizontal(1)).padding([4, 6]));
            }
            let focused = self.focus == Some(entry.id);
            let enabled = entry.action.is_some();
            list = list.push(
                button(
                    row![
                        text(entry.label).size(14).width(Length::Fill),
                        text(entry.detail).size(12).color(if enabled {
                            p.text_secondary
                        } else {
                            p.text_muted
                        }),
                    ]
                    .spacing(16)
                    .align_y(Alignment::Center),
                )
                .padding([6, 12])
                .width(Length::Fill)
                .on_press_maybe(enabled.then_some(Message::MenuItem(entry.id)))
                .style(move |_, status| {
                    let mut style = design::button_style(p, ButtonRole::Menu, focused, status);
                    if !enabled {
                        style.background = Some(p.surface_base.into());
                        style.border.color = iced::Color::TRANSPARENT;
                    }
                    style
                }),
            );
        }
        let x = menu.anchor();
        let panel = container(list)
            .padding(4)
            .width(DROPDOWN_WIDTH)
            .style(move |_| {
                let mut style = design::panel(p.surface_base, p.text_primary, p.border_interactive);
                style.shadow = iced::Shadow {
                    color: iced::Color::BLACK.scale_alpha(0.25),
                    offset: iced::Vector::new(0.0, 4.0),
                    blur_radius: 12.0,
                };
                style
            });
        let backdrop = mouse_area(
            container(Space::new())
                .width(Length::Fill)
                .height(Length::Fill),
        )
        .on_press(Message::Menu(None))
        .interaction(iced::mouse::Interaction::Idle);
        stack![
            backdrop,
            column![
                Space::new().height(BAR_HEIGHT - 2.0),
                row![Space::new().width(x), panel]
            ]
        ]
        .width(Length::Fill)
        .height(Length::Fill)
        .into()
    }
    /// Status strip: operation state on the left, actual project on the right.
    pub(super) fn status_bar(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let (state, color) = if self.closing {
            ("Encerrando · aguarde", p.warning_fg)
        } else if self.busy {
            ("Operação em andamento", p.running_fg)
        } else {
            (self.focused_label().unwrap_or("Pronto"), p.text_secondary)
        };
        let project = self.project_label().map_or_else(
            || "Nenhum projeto aberto".to_owned(),
            |name| format!("Projeto · {name}"),
        );
        column![
            rule::horizontal(1),
            container(
                row![
                    container(icons::icon(icons::Kind::Status)).style(move |_| container::Style {
                        text_color: Some(color),
                        ..Default::default()
                    }),
                    text(state).size(12),
                    space::horizontal(),
                    text(project).size(12).font(HEADING_FONT),
                ]
                .spacing(6)
                .align_y(Alignment::Center),
            )
            .padding([4, 12])
            .width(Length::Fill)
            .style(move |_| container::Style {
                background: Some(p.explorer_bg.into()),
                text_color: Some(p.text_secondary),
                ..Default::default()
            })
        ]
        .into()
    }
}
