//! Native rendering fixture for production button roles; no domain actions.
use iced::widget::{button, column, container, row, text};
use iced::{Element, Length, Theme};
use ox_ui::design::{Appearance, ButtonRole, button_style};

#[derive(Default)]
struct Preview;

const fn update(_: &mut Preview, (): ()) {}

fn appearance() -> Appearance {
    match std::env::args().nth(1).as_deref() {
        Some("dark") => Appearance::Dark,
        Some("hc") => Appearance::HighContrast,
        _ => Appearance::Light,
    }
}

fn view(_: &Preview) -> Element<'_, ()> {
    let p = appearance().palette();
    let mut rows =
        column![text("Production button styles: unfocused / focused").size(22)].spacing(18);
    for (label, role) in [
        ("Primary", ButtonRole::Primary),
        ("Secondary", ButtonRole::Secondary),
        ("Chrome", ButtonRole::Chrome),
        ("Danger", ButtonRole::Danger),
        ("Selected", ButtonRole::Navigation(true)),
        ("Navigation", ButtonRole::Navigation(false)),
    ] {
        let mut controls = row![text(label).width(105)].spacing(12);
        for (state, status) in [
            ("Active", button::Status::Active),
            ("Hover", button::Status::Hovered),
            ("Pressed", button::Status::Pressed),
            ("Disabled", button::Status::Disabled),
        ] {
            let mut pair = row![].spacing(5);
            for focused in [false, true] {
                pair = pair.push(
                    button(text(if focused { "Focus" } else { "Base" }).size(14))
                        .padding([9, 10])
                        .style(move |_, _| button_style(p, role, focused, status)),
                );
            }
            controls = controls.push(column![text(state).size(12), pair].spacing(5));
        }
        rows = rows.push(controls);
    }
    container(rows)
        .padding(24)
        .width(Length::Fill)
        .height(Length::Fill)
        .style(move |_| container::Style {
            background: Some(p.workbench_bg.into()),
            text_color: Some(p.text_primary),
            ..Default::default()
        })
        .into()
}

fn theme(_: &Preview) -> Theme {
    appearance().theme()
}

fn main() -> iced::Result {
    iced::application(Preview::default, update, view)
        .title("Ox audit focus rendering fixture")
        .theme(theme)
        .window_size((1080.0, 640.0))
        .run()
}
