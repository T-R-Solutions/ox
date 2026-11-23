//! Small native line icons; inherit foreground and do not depend on font glyphs.
use crate::workbench::Surface;
use iced::advanced::{Layout, Widget, layout, mouse, renderer, widget::Tree};
use iced::{Color, Element, Length, Rectangle, Size, Theme};

#[derive(Clone, Copy)]
pub(super) enum Kind {
    Folder,
    Repository,
    Plus,
    Panels,
    Search,
    Settings,
    Activity,
    Destination(Surface),
    Close,
    /// Availability notice marker.
    Info,
    /// Extension / plugin entry.
    Plugin,
    /// Downward disclosure chevron.
    Chevron,
    /// Bottom tool-window dock.
    Dock,
    /// Operation status dot.
    Status,
}
struct Icon(Kind);
impl<Message> Widget<Message, Theme, iced::Renderer> for Icon {
    fn size(&self) -> Size<Length> {
        Size::new(Length::Fixed(16.0), Length::Fixed(16.0))
    }
    fn layout(
        &mut self,
        _: &mut Tree,
        _: &iced::Renderer,
        limits: &layout::Limits,
    ) -> layout::Node {
        layout::Node::new(limits.resolve(16, 16, Size::new(16.0, 16.0)))
    }
    fn draw(
        &self,
        _: &Tree,
        renderer: &mut iced::Renderer,
        _: &Theme,
        style: &renderer::Style,
        layout: Layout<'_>,
        _: mouse::Cursor,
        _: &Rectangle,
    ) {
        use iced::advanced::Renderer as _;
        let origin = layout.bounds();
        if matches!(
            self.0,
            Kind::Settings | Kind::Destination(Surface::Settings | Surface::AgentSettings)
        ) {
            draw_cog(renderer, origin, style.text_color);
            return;
        }
        let mut shape = |x: f32, y: f32, w: f32, h: f32, outline: bool| {
            renderer.fill_quad(
                renderer::Quad {
                    bounds: Rectangle {
                        x: origin.x + x,
                        y: origin.y + y,
                        width: w,
                        height: h,
                    },
                    border: iced::Border {
                        color: style.text_color,
                        width: if outline { 1.4 } else { 0.0 },
                        radius: 1.0.into(),
                    },
                    ..Default::default()
                },
                if outline {
                    Color::TRANSPARENT
                } else {
                    style.text_color
                },
            );
        };
        draw_kind(self.0, &mut shape);
    }
}

fn draw_cog(renderer: &mut iced::Renderer, origin: Rectangle, color: Color) {
    use iced::advanced::Renderer as _;
    // One shared cog for every settings entry, independent of font glyphs.
    for n in 0_u8..8 {
        let angle = f32::from(n) * std::f32::consts::FRAC_PI_4;
        renderer.fill_quad(
            renderer::Quad {
                bounds: Rectangle {
                    x: angle.cos().mul_add(5.6, origin.x + 6.8),
                    y: angle.sin().mul_add(5.6, origin.y + 6.8),
                    width: 2.4,
                    height: 2.4,
                },
                border: iced::Border {
                    radius: 0.5.into(),
                    ..Default::default()
                },
                ..Default::default()
            },
            color,
        );
    }
    renderer.fill_quad(
        renderer::Quad {
            bounds: Rectangle {
                x: origin.x + 3.0,
                y: origin.y + 3.0,
                width: 10.0,
                height: 10.0,
            },
            border: iced::Border {
                color,
                width: 3.0,
                radius: 5.0.into(),
            },
            ..Default::default()
        },
        Color::TRANSPARENT,
    );
}

fn draw_kind(kind: Kind, shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    match kind {
        Kind::Folder => {
            shape(1.0, 4.0, 14.0, 10.0, true);
            shape(2.0, 2.0, 6.0, 3.0, true);
        }
        Kind::Plus => {
            shape(7.25, 2.0, 1.5, 12.0, false);
            shape(2.0, 7.25, 12.0, 1.5, false);
        }
        Kind::Panels => {
            shape(1.0, 2.0, 14.0, 12.0, true);
            shape(5.0, 2.0, 1.4, 12.0, false);
        }
        Kind::Search => {
            shape(2.0, 1.0, 10.0, 10.0, true);
            shape(11.0, 11.0, 2.0, 2.0, false);
            shape(13.0, 13.0, 2.0, 2.0, false);
        }
        Kind::Settings => unreachable!("settings use the shared cog"),
        Kind::Repository => {
            shape(2.0, 1.0, 4.0, 4.0, true);
            shape(2.0, 11.0, 4.0, 4.0, true);
            shape(10.0, 1.0, 4.0, 4.0, true);
            shape(3.3, 5.0, 1.4, 6.0, false);
            shape(11.3, 5.0, 1.4, 3.0, false);
            shape(4.0, 7.0, 8.0, 1.4, false);
        }
        Kind::Info => {
            shape(1.0, 1.0, 14.0, 14.0, true);
            shape(7.25, 4.0, 1.5, 1.5, false);
            shape(7.25, 7.0, 1.5, 5.0, false);
        }
        Kind::Plugin => {
            shape(2.0, 5.0, 10.0, 9.0, true);
            shape(5.0, 2.0, 1.4, 3.0, false);
            shape(9.0, 2.0, 1.4, 3.0, false);
            shape(12.0, 8.0, 3.0, 1.4, false);
        }
        Kind::Chevron => {
            for n in 0_u8..5 {
                let f = f32::from(n);
                shape(3.0 + f, 6.0 + f, 1.4, 1.4, false);
                shape(11.6 - f, 6.0 + f, 1.4, 1.4, false);
            }
        }
        Kind::Dock => {
            shape(1.0, 2.0, 14.0, 12.0, true);
            shape(1.0, 9.0, 14.0, 1.4, false);
        }
        Kind::Status => {
            shape(5.0, 5.0, 6.0, 6.0, false);
        }
        Kind::Close => {
            for n in 2_u8..14 {
                let f = f32::from(n);
                shape(f, f, 1.4, 1.4, false);
                shape(15.0 - f, f, 1.4, 1.4, false);
            }
        }
        Kind::Destination(surface) => draw_destination(surface, shape),
        Kind::Activity => {
            for (x, h) in [(2.0, 5.0), (7.0, 11.0), (12.0, 8.0)] {
                shape(x, 14.0 - h, 2.0, h, false);
            }
        }
    }
}

fn draw_destination(surface: Surface, shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    match surface {
        Surface::Start => {
            shape(2.0, 6.0, 12.0, 8.0, true);
            shape(5.0, 2.0, 6.0, 4.0, true);
            shape(7.0, 10.0, 2.0, 4.0, false);
        }
        Surface::NewProject => {
            shape(1.0, 4.0, 14.0, 10.0, true);
            shape(2.0, 2.0, 5.0, 3.0, true);
            shape(7.0, 7.0, 1.4, 5.0, false);
            shape(5.0, 9.0, 5.0, 1.4, false);
        }
        Surface::Project => {
            shape(1.0, 4.0, 14.0, 10.0, true);
            shape(2.0, 2.0, 5.0, 3.0, true);
            shape(4.0, 7.0, 8.0, 1.3, false);
        }
        Surface::Tasks => {
            shape(3.0, 2.0, 11.0, 12.0, true);
            for y in [4.0, 8.0, 12.0] {
                shape(1.0, y, 4.0, 1.2, false);
                shape(7.0, y, 5.0, 1.2, false);
            }
        }
        Surface::NewTask => {
            shape(2.0, 1.0, 10.0, 14.0, true);
            shape(9.0, 7.0, 6.0, 1.4, false);
            shape(11.5, 4.5, 1.4, 6.0, false);
        }
        Surface::Activity => draw_activity(shape),
        Surface::Decisions => {
            shape(2.0, 1.0, 12.0, 10.0, true);
            shape(4.0, 11.0, 2.0, 4.0, false);
            shape(5.0, 4.0, 6.0, 1.4, false);
            shape(5.0, 7.0, 4.0, 1.4, false);
        }
        Surface::Agents => draw_agents(shape),
        Surface::AgentSettings | Surface::Settings => unreachable!("settings use the shared cog"),
        Surface::Providers => draw_providers(shape),
        Surface::Context => draw_context(shape),
        Surface::Tools => {
            shape(2.0, 1.0, 4.0, 6.0, true);
            shape(3.0, 7.0, 2.0, 8.0, false);
            shape(10.0, 1.0, 2.0, 8.0, false);
            shape(9.0, 9.0, 4.0, 6.0, true);
        }
        Surface::Appearance => {
            shape(1.0, 2.0, 14.0, 10.0, true);
            shape(4.0, 5.0, 3.0, 4.0, false);
            shape(9.0, 5.0, 3.0, 4.0, true);
            shape(5.0, 14.0, 6.0, 1.3, false);
        }
        Surface::Editor => {
            shape(1.0, 1.0, 14.0, 14.0, true);
            shape(2.0, 5.0, 12.0, 1.3, false);
            shape(5.0, 6.0, 1.3, 8.0, false);
            shape(8.0, 9.0, 4.0, 1.3, false);
        }
        Surface::Architecture => draw_architecture(shape),
        Surface::Orchestration => draw_orchestration(shape),
        Surface::Observability => draw_observability(shape),
        Surface::Review => draw_review(shape),
        Surface::Recovery => draw_recovery(shape),
        Surface::Focus => {
            for (x, y) in [(1.0, 1.0), (10.0, 1.0), (1.0, 10.0), (10.0, 10.0)] {
                shape(x, y, 5.0, 5.0, true);
            }
            shape(6.0, 6.0, 4.0, 4.0, false);
        }
        Surface::Problems => {
            shape(2.0, 2.0, 12.0, 12.0, true);
            shape(7.0, 4.0, 2.0, 5.0, false);
            shape(7.0, 11.0, 2.0, 1.5, false);
        }
        Surface::Tests => draw_tests(shape),
        Surface::Trace => {
            shape(3.0, 1.0, 1.3, 14.0, false);
            for y in [2.0, 7.0, 12.0] {
                shape(1.0, y, 5.0, 3.0, true);
                shape(8.0, y, 6.0, 1.3, false);
            }
        }
        Surface::Terminal => draw_terminal(shape),
        Surface::Sdd => draw_sdd(shape),
        Surface::Skills => {
            shape(2.0, 1.0, 12.0, 10.0, true);
            shape(4.0, 11.0, 2.0, 4.0, false);
            shape(10.0, 11.0, 2.0, 4.0, false);
            shape(5.0, 4.0, 6.0, 4.0, true);
        }
    }
}

fn draw_architecture(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(5.0, 1.0, 6.0, 4.0, true);
    shape(2.0, 7.0, 12.0, 1.3, false);
    shape(7.0, 5.0, 1.3, 3.0, false);
    shape(2.0, 8.0, 1.3, 3.0, false);
    shape(12.0, 8.0, 1.3, 3.0, false);
    shape(0.0, 11.0, 5.0, 4.0, true);
    shape(10.0, 11.0, 5.0, 4.0, true);
}

fn draw_orchestration(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    for (x, y) in [(1.0, 1.0), (10.0, 1.0), (5.0, 10.0)] {
        shape(x, y, 4.0, 4.0, true);
    }
    shape(5.0, 2.5, 5.0, 1.3, false);
    shape(7.0, 4.0, 1.3, 6.0, false);
    shape(3.0, 7.0, 9.0, 1.3, false);
}

fn draw_activity(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(1.0, 7.0, 3.0, 1.4, false);
    shape(4.0, 4.0, 2.0, 7.0, false);
    shape(7.0, 1.0, 2.0, 13.0, false);
    shape(10.0, 6.0, 2.0, 5.0, false);
    shape(12.0, 8.0, 3.0, 1.4, false);
}

fn draw_recovery(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(1.0, 4.0, 12.0, 10.0, true);
    shape(1.0, 1.0, 1.5, 5.0, false);
    shape(1.0, 1.0, 5.0, 1.5, false);
    shape(6.0, 7.0, 2.0, 3.0, false);
    shape(6.0, 12.0, 2.0, 1.0, false);
}

fn draw_terminal(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(1.0, 2.0, 14.0, 12.0, true);
    shape(4.0, 5.0, 2.0, 2.0, false);
    shape(6.0, 7.0, 2.0, 2.0, false);
    shape(4.0, 9.0, 2.0, 2.0, false);
    shape(9.0, 10.0, 3.0, 1.3, false);
}

fn draw_context(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(1.0, 2.0, 6.0, 12.0, true);
    shape(9.0, 2.0, 6.0, 12.0, true);
    shape(3.0, 5.0, 2.0, 1.0, false);
    shape(11.0, 5.0, 2.0, 1.0, false);
    shape(7.0, 3.0, 2.0, 12.0, false);
}

fn draw_agents(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(3.0, 4.0, 10.0, 9.0, true);
    shape(7.0, 1.0, 2.0, 3.0, false);
    shape(5.0, 7.0, 2.0, 2.0, false);
    shape(10.0, 7.0, 2.0, 2.0, false);
    shape(6.0, 11.0, 4.0, 1.0, false);
}

fn draw_review(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(1.0, 1.0, 6.0, 14.0, true);
    shape(9.0, 1.0, 6.0, 14.0, true);
    shape(3.0, 5.0, 2.0, 1.3, false);
    shape(11.0, 8.0, 2.0, 1.3, false);
    shape(11.0, 5.0, 2.0, 1.3, false);
}

fn draw_tests(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(4.0, 1.0, 8.0, 2.0, false);
    shape(5.0, 3.0, 1.3, 6.0, false);
    shape(10.0, 3.0, 1.3, 6.0, false);
    shape(3.0, 8.0, 10.0, 7.0, true);
    shape(5.0, 11.0, 6.0, 2.0, false);
}

fn draw_sdd(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(2.0, 1.0, 12.0, 14.0, true);
    shape(4.0, 4.0, 3.0, 3.0, true);
    shape(9.0, 4.0, 3.0, 1.3, false);
    shape(4.0, 10.0, 3.0, 3.0, true);
    shape(9.0, 10.0, 3.0, 1.3, false);
}

fn draw_providers(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    for (x, y) in [(1.0, 1.0), (9.0, 1.0), (5.0, 10.0)] {
        shape(x, y, 6.0, 5.0, true);
    }
    shape(3.0, 7.0, 10.0, 1.3, false);
    shape(7.0, 6.0, 1.3, 5.0, false);
}

fn draw_observability(shape: &mut impl FnMut(f32, f32, f32, f32, bool)) {
    shape(1.0, 1.0, 14.0, 14.0, true);
    shape(4.0, 9.0, 2.0, 4.0, false);
    shape(7.0, 5.0, 2.0, 8.0, false);
    shape(10.0, 3.0, 2.0, 10.0, false);
}
pub(super) fn icon<'a, Message: 'a>(kind: Kind) -> Element<'a, Message> {
    Element::new(Icon(kind))
}
