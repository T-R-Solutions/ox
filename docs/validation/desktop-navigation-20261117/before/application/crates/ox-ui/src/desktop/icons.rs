//! Small native line icons; inherit foreground and do not depend on font glyphs.
use iced::advanced::{Layout, Widget, layout, mouse, renderer, widget::Tree};
use iced::{Color, Element, Length, Rectangle, Size, Theme};

#[derive(Clone, Copy)]
pub(super) enum Kind {
    Folder,
    Plus,
    Panels,
    Search,
    Settings,
    File,
    Activity,
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
        match self.0 {
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
            Kind::Settings => {
                for (y, x) in [(3.0, 4.0), (8.0, 10.0), (13.0, 6.0)] {
                    shape(1.0, y, 14.0, 1.3, false);
                    shape(x, y - 2.0, 3.0, 5.0, true);
                }
            }
            Kind::File => {
                shape(3.0, 1.0, 10.0, 14.0, true);
                shape(5.0, 5.0, 6.0, 1.3, false);
                shape(5.0, 8.0, 6.0, 1.3, false);
                shape(5.0, 11.0, 4.0, 1.3, false);
            }
            Kind::Activity => {
                for (x, h) in [(2.0, 5.0), (7.0, 11.0), (12.0, 8.0)] {
                    shape(x, 14.0 - h, 2.0, h, false);
                }
            }
        }
    }
}
pub(super) fn icon<'a, Message: 'a>(kind: Kind) -> Element<'a, Message> {
    Element::new(Icon(kind))
}
