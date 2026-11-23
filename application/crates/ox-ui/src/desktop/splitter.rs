//! Sidebar handle; drag lifetime is owned by Desktop's global event subscription.
use super::Message;
use iced::advanced::{Widget, layout, mouse, renderer, widget::Tree};
use iced::{Color, Element, Length, Rectangle, Size, Theme};
struct Splitter {
    /// Decorative separator color while idle.
    rest: Color,
    /// Interaction color while hovered or dragged.
    color: Color,
    active: bool,
}
impl Widget<Message, Theme, iced::Renderer> for Splitter {
    fn size(&self) -> Size<Length> {
        Size::new(Length::Fixed(6.0), Length::Fill)
    }
    fn layout(
        &mut self,
        _: &mut Tree,
        _: &iced::Renderer,
        limits: &layout::Limits,
    ) -> layout::Node {
        layout::Node::new(limits.resolve(6, Length::Fill, Size::ZERO))
    }
    fn update(
        &mut self,
        _: &mut Tree,
        event: &iced::Event,
        layout: iced::advanced::Layout<'_>,
        cursor: mouse::Cursor,
        _: &iced::Renderer,
        _: &mut dyn iced::advanced::Clipboard,
        shell: &mut iced::advanced::Shell<'_, Message>,
        _: &Rectangle,
    ) {
        if matches!(
            event,
            iced::Event::Mouse(mouse::Event::ButtonPressed(mouse::Button::Left))
        ) && cursor.is_over(layout.bounds())
        {
            shell.publish(Message::SidebarStart(
                cursor.position().map_or(0.0, |p| p.x - layout.bounds().x),
            ));
            shell.capture_event();
        }
    }
    fn draw(
        &self,
        _: &Tree,
        renderer: &mut iced::Renderer,
        _: &Theme,
        _: &renderer::Style,
        layout: iced::advanced::Layout<'_>,
        cursor: mouse::Cursor,
        _: &Rectangle,
    ) {
        use iced::advanced::Renderer as _;
        let b = layout.bounds();
        let engaged = self.active || cursor.is_over(b);
        renderer.fill_quad(
            renderer::Quad {
                bounds: Rectangle {
                    x: b.x
                        + if self.active || cursor.is_over(b) {
                            1.0
                        } else {
                            2.5
                        },
                    y: b.y,
                    width: if self.active || cursor.is_over(b) {
                        4.0
                    } else {
                        1.0
                    },
                    height: b.height,
                },
                ..Default::default()
            },
            if engaged { self.color } else { self.rest },
        );
    }
    fn mouse_interaction(
        &self,
        _: &Tree,
        layout: iced::advanced::Layout<'_>,
        cursor: mouse::Cursor,
        _: &Rectangle,
        _: &iced::Renderer,
    ) -> mouse::Interaction {
        if self.active || cursor.is_over(layout.bounds()) {
            mouse::Interaction::ResizingHorizontally
        } else {
            mouse::Interaction::None
        }
    }
}
pub(super) fn divider<'a>(rest: Color, color: Color, active: bool) -> Element<'a, Message> {
    Element::new(Splitter {
        rest,
        color,
        active,
    })
}
