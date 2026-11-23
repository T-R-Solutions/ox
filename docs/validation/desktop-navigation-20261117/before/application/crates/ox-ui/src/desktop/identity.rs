//! Supplied identity, embedded so the executable never depends on `.local/assets`.
use iced::widget::image::Handle;
use std::sync::OnceLock;

pub(super) fn signature(high_contrast: bool) -> Handle {
    static COLOR: OnceLock<Handle> = OnceLock::new();
    static WHITE: OnceLock<Handle> = OnceLock::new();
    if high_contrast {
        WHITE
            .get_or_init(|| {
                Handle::from_bytes(
                    include_bytes!("../../assets/identity/logo-branco.png").as_slice(),
                )
            })
            .clone()
    } else {
        COLOR
            .get_or_init(|| {
                Handle::from_bytes(
                    include_bytes!("../../assets/identity/logo-escuro.png").as_slice(),
                )
            })
            .clone()
    }
}

pub(super) fn mascot() -> Handle {
    static MASCOT: OnceLock<Handle> = OnceLock::new();
    MASCOT
        .get_or_init(|| {
            Handle::from_bytes(include_bytes!("../../assets/identity/mascote-ox.png").as_slice())
        })
        .clone()
}
