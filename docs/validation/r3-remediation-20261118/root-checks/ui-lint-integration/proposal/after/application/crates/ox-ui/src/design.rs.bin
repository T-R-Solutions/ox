//! Native presentation roles. Functional state stays in Controller/Runtime/Engine.
use crate::tokens::{self, Palette};
use iced::{
    Border, Color, Theme, font,
    widget::{button, container, scrollable, text_input},
};

pub const UI_FONT: iced::Font = iced::Font::with_name("IBM Plex Sans");
pub const CODE_FONT: iced::Font = iced::Font::with_name("IBM Plex Mono");
pub const HEADING_FONT: iced::Font = iced::Font {
    weight: font::Weight::Semibold,
    ..UI_FONT
};

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum Appearance {
    #[default]
    Light,
    Dark,
    HighContrast,
}
impl Appearance {
    pub const ALL: [Self; 3] = [Self::Light, Self::Dark, Self::HighContrast];
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::Light => "Claro",
            Self::Dark => "Escuro · candidato",
            Self::HighContrast => "Alto contraste · candidato",
        }
    }
    #[must_use]
    pub const fn next(self) -> Self {
        match self {
            Self::Light => Self::Dark,
            Self::Dark => Self::HighContrast,
            Self::HighContrast => Self::Light,
        }
    }
    #[must_use]
    pub const fn palette(self) -> Palette {
        match self {
            Self::Light => tokens::LIGHT,
            Self::Dark => tokens::DARK,
            Self::HighContrast => tokens::HC,
        }
    }
    #[must_use]
    pub fn theme(self) -> Theme {
        let p = self.palette();
        Theme::custom(
            format!("Ox {}", self.label()),
            iced::theme::Palette {
                background: p.workbench_bg,
                text: p.text_primary,
                primary: p.action_bg,
                success: p.success_fg,
                danger: p.error_fg,
                warning: p.warning_fg,
            },
        )
    }
}

#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum Density {
    #[default]
    Comfortable,
    Compact,
}
impl Density {
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::Comfortable => "Confortável",
            Self::Compact => "Compacta",
        }
    }
    #[must_use]
    pub const fn next(self) -> Self {
        match self {
            Self::Comfortable => Self::Compact,
            Self::Compact => Self::Comfortable,
        }
    }
    #[must_use]
    pub const fn gap(self) -> f32 {
        match self {
            Self::Comfortable => 12.0,
            Self::Compact => 8.0,
        }
    }
    #[must_use]
    pub const fn inset(self) -> f32 {
        match self {
            Self::Comfortable => 20.0,
            Self::Compact => 12.0,
        }
    }
    #[must_use]
    pub const fn control_padding(self) -> [u16; 2] {
        match self {
            Self::Comfortable => [7, 12],
            Self::Compact => [5, 10],
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub enum ButtonRole {
    Primary,
    Secondary,
    Navigation(bool),
    Chrome,
    Danger,
    /// Item inside an open command menu.
    Menu,
    /// Document or tool-window tab; `true` is the active tab.
    Tab(bool),
}

#[must_use]
pub fn button_style(
    p: Palette,
    role: ButtonRole,
    focused: bool,
    status: button::Status,
) -> button::Style {
    let disabled = status == button::Status::Disabled;
    let hovered = matches!(status, button::Status::Hovered | button::Status::Pressed);
    let (mut bg, mut fg, mut border) = match role {
        ButtonRole::Primary => (p.action_bg, p.action_text, p.action_bg),
        ButtonRole::Secondary => (p.surface_base, p.text_primary, p.border_interactive),
        // Selection is carried by the fill and the separate side marker; the
        // perimeter is reserved for keyboard focus so both remain distinct.
        ButtonRole::Navigation(true) => (p.surface_selected, p.text_primary, Color::TRANSPARENT),
        ButtonRole::Navigation(false) | ButtonRole::Tab(false) => {
            (p.explorer_bg, p.text_secondary, Color::TRANSPARENT)
        }
        ButtonRole::Chrome => (p.shell_bg, p.text_shell, Color::TRANSPARENT),
        ButtonRole::Danger => (p.error_bg, p.error_fg, p.error_fg),
        ButtonRole::Menu | ButtonRole::Tab(true) => {
            (p.surface_base, p.text_primary, Color::TRANSPARENT)
        }
    };
    if hovered && !disabled {
        bg = match role {
            ButtonRole::Primary => p.action_hover,
            ButtonRole::Chrome => p.shell_deep,
            ButtonRole::Navigation(true) => p.surface_selected,
            _ => p.surface_recessed,
        };
    }
    if disabled {
        bg = p.surface_recessed;
        fg = p.text_muted;
        border = p.border_decorative;
    }
    if focused && !disabled {
        // Focus is an additional boundary, never a replacement for role or interaction.
        border = match role {
            ButtonRole::Primary | ButtonRole::Chrome => fg,
            _ => p.focus,
        };
    }
    button::Style {
        background: Some(bg.into()),
        text_color: fg,
        border: Border {
            color: border,
            width: if !disabled && (focused || status == button::Status::Pressed) {
                2.0
            } else {
                1.0
            },
            radius: 4.0.into(),
        },
        ..Default::default()
    }
}

#[must_use]
pub fn input_style(p: Palette, status: text_input::Status) -> text_input::Style {
    let focused = matches!(status, text_input::Status::Focused { .. });
    let disabled = matches!(status, text_input::Status::Disabled);
    text_input::Style {
        background: if disabled {
            p.surface_recessed
        } else {
            p.surface_base
        }
        .into(),
        border: Border {
            color: if disabled {
                p.border_decorative
            } else if focused {
                p.focus
            } else {
                p.border_interactive
            },
            width: if focused { 2.0 } else { 1.0 },
            radius: 4.0.into(),
        },
        icon: if disabled {
            p.text_muted
        } else {
            p.icon_primary
        },
        placeholder: p.text_muted,
        value: if disabled {
            p.text_muted
        } else {
            p.text_primary
        },
        selection: p.surface_selected,
    }
}

/// Thin neutral scrollbar shared by docked regions. The scroller keeps a
/// functional boundary color; the rail stays decorative.
pub fn scrollable_style(p: Palette) -> impl Fn(&Theme, scrollable::Status) -> scrollable::Style {
    move |_, status| {
        let active = matches!(
            status,
            scrollable::Status::Hovered {
                is_vertical_scrollbar_hovered: true,
                ..
            } | scrollable::Status::Dragged {
                is_vertical_scrollbar_dragged: true,
                ..
            }
        );
        let rail = scrollable::Rail {
            background: None,
            border: Border::default(),
            scroller: scrollable::Scroller {
                background: if active {
                    p.border_interactive
                } else {
                    p.border_neutral
                }
                .into(),
                border: Border {
                    radius: 3.0.into(),
                    ..Border::default()
                },
            },
        };
        scrollable::Style {
            container: container::Style::default(),
            vertical_rail: rail,
            horizontal_rail: rail,
            gap: None,
            auto_scroll: scrollable::AutoScroll {
                background: p.surface_base.into(),
                border: Border {
                    color: p.border_interactive,
                    width: 1.0,
                    radius: 4.0.into(),
                },
                shadow: iced::Shadow::default(),
                icon: p.icon_primary,
            },
        }
    }
}

/// Thin vertical scrollbar geometry used with [`scrollable_style`].
#[must_use]
pub fn thin_scrollbar() -> scrollable::Direction {
    scrollable::Direction::Vertical(scrollable::Scrollbar::new().width(6).scroller_width(6))
}

/// Single page-level availability banner: a solid brand stripe plus a
/// recessed surface, so it does not rely on hue alone.
#[must_use]
pub fn info_bar(p: Palette) -> container::Style {
    container::Style {
        background: Some(p.surface_recessed.into()),
        text_color: Some(p.text_primary),
        border: Border {
            color: Color::TRANSPARENT,
            width: 0.0,
            radius: 4.0.into(),
        },
        ..Default::default()
    }
}

/// Recessed note inside a section: no decorative frame.
#[must_use]
pub fn note(p: Palette) -> container::Style {
    container::Style {
        background: Some(p.surface_recessed.into()),
        text_color: Some(p.text_secondary),
        border: Border {
            radius: 4.0.into(),
            ..Border::default()
        },
        ..Default::default()
    }
}

#[must_use]
pub fn panel(background: Color, foreground: Color, border: Color) -> container::Style {
    container::Style {
        background: Some(background.into()),
        text_color: Some(foreground),
        border: Border {
            color: border,
            width: 1.0,
            radius: 6.0.into(),
        },
        ..Default::default()
    }
}

/// Only the first Controller status line is used for the current verdict.
/// A historical APPROVED line can never recolor a current stale result green.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceState {
    Unverified,
    Approved,
    Rejected,
    Inconclusive,
    NotApplicable,
}
impl EvidenceState {
    #[must_use]
    pub fn from_status(raw: &str) -> Self {
        match raw.lines().next().unwrap_or_default() {
            "APPROVED" | "Critério aprovado" => Self::Approved,
            "REJECTED" | "Critério reprovado" => Self::Rejected,
            "INCONCLUSIVE" | "Inconclusivo" => Self::Inconclusive,
            "NOT APPLICABLE" | "Não aplicável" => Self::NotApplicable,
            _ => Self::Unverified,
        }
    }
    #[must_use]
    pub const fn label(self) -> &'static str {
        match self {
            Self::Unverified => "Não verificado",
            Self::Approved => "Critério aprovado",
            Self::Rejected => "Critério reprovado",
            Self::Inconclusive => "Inconclusivo",
            Self::NotApplicable => "Não aplicável",
        }
    }
    #[must_use]
    pub const fn colors(self, p: Palette) -> (Color, Color) {
        match self {
            Self::Approved => (p.success_fg, p.success_bg),
            Self::Rejected => (p.error_fg, p.error_bg),
            Self::Inconclusive => (p.warning_fg, p.warning_bg),
            _ => (p.unknown_fg, p.unknown_bg),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn contrast(a: Color, b: Color) -> f32 {
        let luminance = |c: Color| {
            let linear = |v: f32| {
                if v <= 0.04045 {
                    v / 12.92
                } else {
                    ((v + 0.055) / 1.055).powf(2.4)
                }
            };
            0.0722_f32.mul_add(
                linear(c.b),
                0.7152_f32.mul_add(linear(c.g), 0.2126 * linear(c.r)),
            )
        };
        let (a, b) = (luminance(a), luminance(b));
        (a.max(b) + 0.05) / (a.min(b) + 0.05)
    }

    #[test]
    fn focused_button_boundary_and_label_remain_visible_in_every_role_and_theme() {
        for appearance in Appearance::ALL {
            let p = appearance.palette();
            for role in [
                ButtonRole::Primary,
                ButtonRole::Secondary,
                ButtonRole::Chrome,
                ButtonRole::Danger,
                ButtonRole::Navigation(true),
                ButtonRole::Navigation(false),
                ButtonRole::Menu,
                ButtonRole::Tab(true),
                ButtonRole::Tab(false),
            ] {
                for state in [
                    button::Status::Active,
                    button::Status::Hovered,
                    button::Status::Pressed,
                ] {
                    let style = button_style(p, role, true, state);
                    let Some(iced::Background::Color(background)) = style.background else {
                        panic!("focused control must have an opaque background");
                    };
                    assert!(contrast(style.border.color, background) >= 3.0);
                    assert!(contrast(style.text_color, background) >= 4.5);
                }
            }
        }
    }

    #[test]
    fn focus_preserves_role_and_interaction_colors_in_every_theme() {
        for appearance in Appearance::ALL {
            let p = appearance.palette();
            for role in [
                ButtonRole::Primary,
                ButtonRole::Secondary,
                ButtonRole::Chrome,
                ButtonRole::Danger,
                ButtonRole::Navigation(true),
                ButtonRole::Navigation(false),
                ButtonRole::Menu,
                ButtonRole::Tab(true),
                ButtonRole::Tab(false),
            ] {
                for status in [
                    button::Status::Active,
                    button::Status::Hovered,
                    button::Status::Pressed,
                    button::Status::Disabled,
                ] {
                    let unfocused = button_style(p, role, false, status);
                    let focused = button_style(p, role, true, status);
                    assert_eq!(focused.background, unfocused.background);
                    assert_eq!(focused.text_color, unfocused.text_color);
                    if status == button::Status::Disabled {
                        assert_eq!(focused.border, unfocused.border);
                    } else {
                        assert_eq!(focused.border.width, 2.0);
                    }
                }
            }
            for role in [ButtonRole::Primary, ButtonRole::Chrome] {
                assert_ne!(
                    button_style(p, role, true, button::Status::Active).background,
                    button_style(p, role, true, button::Status::Hovered).background
                );
            }
        }
    }

    #[test]
    fn focus_preserves_selection_and_disabled_inputs_remain_distinct() {
        for appearance in Appearance::ALL {
            let p = appearance.palette();
            for status in [
                button::Status::Active,
                button::Status::Hovered,
                button::Status::Pressed,
            ] {
                let selected = button_style(p, ButtonRole::Navigation(true), true, status);
                let other = button_style(p, ButtonRole::Navigation(false), true, status);
                assert_ne!(selected.background, other.background);
                assert_eq!(selected.border.color, other.border.color);
            }
            let active = input_style(p, text_input::Status::Active);
            let disabled = input_style(p, text_input::Status::Disabled);
            assert_ne!(active.background, disabled.background);
            assert_ne!(active.value, disabled.value);
        }
    }

    #[test]
    fn historical_approval_never_approves_current_stale_or_missing_inputs() {
        assert_eq!(
            EvidenceState::from_status(
                "Não verificado / entradas alteradas ou ausentes\nHistórico:\nCritério aprovado"
            ),
            EvidenceState::Unverified
        );
        for (status, expected) in [
            ("Critério aprovado", EvidenceState::Approved),
            ("Critério reprovado", EvidenceState::Rejected),
            ("Inconclusivo", EvidenceState::Inconclusive),
            ("Não aplicável", EvidenceState::NotApplicable),
        ] {
            assert_eq!(EvidenceState::from_status(status), expected);
        }
        assert_eq!(
            EvidenceState::from_status("UNVERIFIED / stale or missing\nHistory:\nAPPROVED"),
            EvidenceState::Unverified
        );
        assert_eq!(
            EvidenceState::from_status("Attempt 2: Success; observed exit. UNVERIFIED."),
            EvidenceState::Unverified
        );
        assert_eq!(
            EvidenceState::from_status("REJECTED\nHistory: APPROVED"),
            EvidenceState::Rejected
        );
        assert_eq!(
            EvidenceState::from_status("APPROVED\nCriterion: result:1"),
            EvidenceState::Approved
        );
    }
}
