#[derive(Debug, Default)]
pub struct Shell {
    details_visible: bool,
}
#[derive(Debug, Clone, Copy)]
pub enum Message {
    ToggleDetails,
    Exit,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Effect {
    None,
    Exit,
}
impl Shell {
    pub fn details_visible(&self) -> bool {
        self.details_visible
    }
    pub fn update(&mut self, message: Message) -> Effect {
        match message {
            Message::ToggleDetails => {
                self.details_visible = !self.details_visible;
                Effect::None
            }
            Message::Exit => Effect::Exit,
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn toggle_roundtrip() {
        let mut s = Shell::default();
        assert!(!s.details_visible);
        assert_eq!(s.update(Message::ToggleDetails), Effect::None);
        assert!(s.details_visible);
        s.update(Message::ToggleDetails);
        assert!(!s.details_visible);
    }
}
