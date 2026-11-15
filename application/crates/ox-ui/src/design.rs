//! Native presentation roles. Functional state stays in Controller/Runtime/Engine.
use crate::tokens::{self, Palette};
use iced::{
    Border, Color, Theme, font,
    widget::{button, container},
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
        ButtonRole::Navigation(true) => (p.surface_selected, p.text_primary, p.selection_indicator),
        ButtonRole::Navigation(false) => (p.explorer_bg, p.text_secondary, Color::TRANSPARENT),
        ButtonRole::Chrome => (p.shell_bg, p.text_shell, Color::TRANSPARENT),
        ButtonRole::Danger => (p.error_bg, p.error_fg, p.error_fg),
    };
    if hovered && !disabled {
        bg = match role {
            ButtonRole::Primary => p.action_hover,
            ButtonRole::Chrome => p.shell_deep,
            _ => p.surface_recessed,
        };
    }
    if disabled {
        bg = p.surface_recessed;
        fg = p.text_muted;
        border = p.border_decorative;
    }
    if focused && !disabled {
        border = match role {
            ButtonRole::Primary | ButtonRole::Chrome => p.text_shell,
            _ => p.focus,
        };
    }
    button::Style {
        background: Some(bg.into()),
        text_color: fg,
        border: Border {
            color: border,
            width: if focused { 2.0 } else { 1.0 },
            radius: 4.0.into(),
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
            "APPROVED" => Self::Approved,
            "REJECTED" => Self::Rejected,
            "INCONCLUSIVE" => Self::Inconclusive,
            "NOT APPLICABLE" => Self::NotApplicable,
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
    #[test]
    fn historical_approval_never_approves_current_stale_or_missing_inputs() {
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
