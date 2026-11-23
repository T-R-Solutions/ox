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

#[cfg(test)]
mod tests {
    #[test]
    fn embedded_signatures_decode_with_the_enabled_png_codec() {
        for bytes in [
            include_bytes!("../../assets/identity/logo-branco.png").as_slice(),
            include_bytes!("../../assets/identity/logo-escuro.png").as_slice(),
        ] {
            let image = image::load_from_memory(bytes).expect("bundled PNG must decode");
            assert_eq!((image.width(), image.height()), (960, 300));
        }
    }
}
