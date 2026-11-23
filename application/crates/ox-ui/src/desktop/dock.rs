//! Document tabs over the primary canvas and the bottom tool-window dock.
//! Both are session presentation state; selecting or closing never starts,
//! cancels or discards domain work.
use super::{Desktop, Message, icons};
use crate::design::{self, ButtonRole};
use crate::workbench::Surface;
use iced::widget::{Space, button, column, container, row, rule, scrollable, space, text};
use iced::{Alignment, Element, Length, Task};

/// Tool windows hosted by the bottom dock, in tab order (ids 640–643).
pub(super) const DOCK_TOOLS: [Surface; 4] = [
    Surface::Problems,
    Surface::Tests,
    Surface::Trace,
    Surface::Terminal,
];
const MAX_TABS: usize = 8;

/// Destinations that open as documents in the primary canvas.
pub(super) fn tab_eligible(surface: Surface) -> bool {
    !matches!(
        surface,
        Surface::Start | Surface::NewProject | Surface::Settings | Surface::Appearance
    ) && !DOCK_TOOLS.contains(&surface)
}
fn tab_id(surface: Surface) -> usize {
    500 + 2 * surface.index()
}

impl Desktop {
    /// Open tabs plus the active document when it was reached without a tab
    /// (for example after initialization), so the strip is never empty.
    pub(super) fn visible_tabs(&self) -> Vec<Surface> {
        let mut tabs = self.tabs.clone();
        if tab_eligible(self.surface) && !tabs.contains(&self.surface) {
            tabs.push(self.surface);
        }
        tabs
    }
    pub(super) fn open_tab(&mut self, surface: Surface) {
        if !tab_eligible(surface) {
            return;
        }
        if !self.tabs.contains(&surface) {
            self.tabs.push(surface);
        }
        while self.tabs.len() > MAX_TABS {
            let oldest = self
                .tabs
                .iter()
                .position(|s| *s != surface)
                .expect("more than one tab");
            self.tabs.remove(oldest);
        }
    }
    /// Closes a document tab. The last document cannot be closed, and closing
    /// the active tab activates its neighbor.
    pub(super) fn close_tab(&mut self, surface: Surface) -> Task<Message> {
        let tabs = self.visible_tabs();
        let Some(position) = tabs.iter().position(|s| *s == surface) else {
            return Task::none();
        };
        if tabs.len() <= 1 {
            return Task::none();
        }
        self.tabs = tabs;
        self.tabs.remove(position);
        if self.surface == surface {
            let neighbor = self.tabs[position.min(self.tabs.len() - 1)];
            // The closed document must not be re-registered as the one being left.
            self.surface = neighbor;
            self.focus = Some(tab_id(neighbor));
            return self.update(Message::Navigate(neighbor));
        }
        self.restore_visible_focus();
        Task::none()
    }
    pub(super) fn tab_controls(&self) -> Vec<(usize, Message)> {
        let tabs = self.visible_tabs();
        let closable = tabs.len() > 1;
        let mut controls = Vec::new();
        for surface in tabs {
            controls.push((tab_id(surface), Message::Navigate(surface)));
            if closable {
                controls.push((tab_id(surface) + 1, Message::CloseTab(surface)));
            }
        }
        controls
    }
    pub(super) fn dock_controls(&self) -> Vec<(usize, Message)> {
        if !self.dock_visible() {
            return Vec::new();
        }
        let mut controls: Vec<_> = DOCK_TOOLS
            .iter()
            .enumerate()
            .map(|(i, s)| (640 + i, Message::Navigate(*s)))
            .collect();
        controls.push((645, Message::Dock));
        controls
    }
    pub(super) fn dock_visible(&self) -> bool {
        self.dock_open && self.surface != Surface::Focus
    }
    pub(super) fn tab_strip(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let tabs = self.visible_tabs();
        let closable = tabs.len() > 1;
        let mut strip = row![].spacing(1);
        for surface in tabs {
            let active = surface == self.surface;
            let id = tab_id(surface);
            let focused = self.focus == Some(id);
            let mut tab = row![
                button(
                    text(surface.title())
                        .size(13)
                        .wrapping(text::Wrapping::None)
                )
                .padding([7, 12])
                .on_press(Message::Navigate(surface))
                .style(move |_, status| {
                    design::button_style(p, ButtonRole::Tab(active), focused, status)
                })
            ]
            .align_y(Alignment::Center);
            if closable {
                let close_focused = self.focus == Some(id + 1);
                tab = tab.push(
                    iced::widget::tooltip(
                        button(icons::icon(icons::Kind::Close))
                            .padding(5)
                            .on_press(Message::CloseTab(surface))
                            .style(move |_, status| {
                                design::button_style(
                                    p,
                                    ButtonRole::Tab(active),
                                    close_focused,
                                    status,
                                )
                            }),
                        container(text(format!("Fechar {}", surface.title())).size(13))
                            .padding(8)
                            .style(move |_| {
                                design::panel(p.surface_base, p.text_primary, p.border_interactive)
                            }),
                        iced::widget::tooltip::Position::Bottom,
                    )
                    .gap(4),
                );
            }
            // Active document: 2-unit top marker plus base surface and text,
            // so the state never depends on hue alone.
            let marker = container(Space::new().width(Length::Fill).height(2)).style(move |_| {
                container::Style {
                    background: active.then_some(p.selection_indicator.into()),
                    ..Default::default()
                }
            });
            strip = strip.push(
                // The tab row sizes the stack; the marker overlays its top edge
                // without stretching the tab to the strip width.
                container(iced::widget::stack![
                    container(tab).padding(iced::Padding {
                        top: 2.0,
                        ..iced::Padding::ZERO
                    }),
                    column![marker]
                ])
                .style(move |_| container::Style {
                    background: Some(
                        if active {
                            p.surface_base
                        } else {
                            p.explorer_bg
                        }
                        .into(),
                    ),
                    ..Default::default()
                })
                .padding([0, 2]),
            );
        }
        column![
            container(strip.wrap())
                .width(Length::Fill)
                .padding([0, 4])
                .style(move |_| container::Style {
                    background: Some(p.explorer_bg.into()),
                    ..Default::default()
                }),
            rule::horizontal(1)
        ]
        .into()
    }
    pub(super) fn dock_panel(&self) -> Element<'_, Message> {
        let p = self.appearance.palette();
        let mut tabs = row![].spacing(1).align_y(Alignment::Center);
        for (i, surface) in DOCK_TOOLS.iter().enumerate() {
            let active = *surface == self.dock_tool;
            let focused = self.focus == Some(640 + i);
            tabs = tabs.push(
                button(text(surface.title()).size(13))
                    .padding([6, 12])
                    .on_press(Message::Navigate(*surface))
                    .style(move |_, status| {
                        let mut style =
                            design::button_style(p, ButtonRole::Tab(active), focused, status);
                        if active && !focused {
                            // Underline-equivalent: a solid boundary on the active tool.
                            style.border.color = p.selection_indicator;
                        }
                        style
                    }),
            );
        }
        let mut header = row![
            text("FERRAMENTAS").size(12).color(p.text_muted),
            tabs,
            space::horizontal()
        ]
        .spacing(12)
        .align_y(Alignment::Center);
        if matches!(self.dock_tool, Surface::Tests | Surface::Trace) {
            header = header.push(self.evidence_badge());
        }
        header = header.push(self.icon_control(
            645,
            "Ocultar painel de ferramentas",
            icons::Kind::Close,
            Message::Dock,
        ));
        column![
            rule::horizontal(1),
            container(header)
                .padding([4, 12])
                .width(Length::Fill)
                .style(move |_| container::Style {
                    background: Some(p.explorer_bg.into()),
                    ..Default::default()
                }),
            scrollable(
                container(self.tool_content(self.dock_tool))
                    .padding([8, 12])
                    .width(Length::Fill)
            )
            .id("dock")
            .direction(design::thin_scrollbar())
            .style(design::scrollable_style(p))
            .height(Length::Fill)
        ]
        // 30% of the work area, so short windows keep the document usable.
        .height(Length::FillPortion(3))
        .into()
    }
}
