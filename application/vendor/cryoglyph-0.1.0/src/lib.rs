//! Glyphon provides a simple way to render 2D text with [wgpu], [cosmic-text] and [etagere].
//!
//! [wpgu]: https://github.com/gfx-rs/wgpu
//! [cosmic-text]: https://github.com/pop-os/cosmic-text
//! [etagere]: https://github.com/nical/etagere

mod cache;
mod error;
mod text_atlas;
mod text_render;
mod viewport;

pub use cache::Cache;
pub use error::{PrepareError, RenderError};
pub use text_atlas::{ColorMode, TextAtlas};
pub use text_render::TextRenderer;
pub use viewport::Viewport;

use text_render::ContentType;

// Re-export all top-level types from `cosmic-text` for convenience.
#[doc(no_inline)]
pub use cosmic_text::{
    self, Action, Affinity, Attrs, AttrsList, AttrsOwned, Buffer, BufferLine, CacheKey, Color,
    Command, Cursor, Edit, Editor, Family, FamilyOwned, Font, FontSystem, LayoutCursor,
    LayoutGlyph, LayoutLine, LayoutRun, LayoutRunIter, Metrics, ShapeGlyph, ShapeLine, ShapeSpan,
    ShapeWord, Shaping, Stretch, Style, SubpixelBin, SwashCache, SwashContent, SwashImage, Weight,
    Wrap, fontdb,
};

use etagere::AllocId;

pub(crate) enum GpuCacheStatus {
    InAtlas {
        x: u16,
        y: u16,
        content_type: ContentType,
    },
    SkipRasterization,
}

pub(crate) struct GlyphDetails {
    width: u16,
    height: u16,
    gpu_cache: GpuCacheStatus,
    atlas_id: Option<AllocId>,
    top: i16,
    left: i16,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, bytemuck::Pod, bytemuck::Zeroable)]
pub(crate) struct GlyphToRender {
    pos: [i32; 2],
    dim: [u16; 2],
    uv: [u16; 2],
    color: u32,
    content_type_with_srgb: [u16; 2],
    depth: f32,
}

/// The screen resolution to use when rendering text.
#[repr(C)]
#[derive(Clone, Copy, Debug, Eq, PartialEq, bytemuck::Pod, bytemuck::Zeroable)]
pub struct Resolution {
    /// The width of the screen in pixels.
    pub width: u32,
    /// The height of the screen in pixels.
    pub height: u32,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Eq, PartialEq, bytemuck::Pod, bytemuck::Zeroable)]
pub(crate) struct Params {
    screen_resolution: Resolution,
    _pad: [u32; 2],
}

#[cfg(test)]
mod ox_layout_tests {
    use super::{GlyphToRender, Params, Resolution};
    use std::mem::{offset_of, size_of};

    fn glyph(depth_bits: u32) -> GlyphToRender {
        GlyphToRender {
            pos: [i32::MIN, i32::MAX],
            dim: [0, u16::MAX],
            uv: [1, 0xabcd],
            color: 0x1122_3344,
            content_type_with_srgb: [1, 2],
            depth: f32::from_bits(depth_bits),
        }
    }

    // Independent field encoding follows the GPU vertex attributes in cache.rs.
    fn expected_glyph(value: &GlyphToRender) -> Vec<u8> {
        let mut expected = Vec::new();
        for position in value.pos {
            expected.extend_from_slice(&position.to_ne_bytes());
        }
        for dimension in value.dim {
            expected.extend_from_slice(&dimension.to_ne_bytes());
        }
        for coordinate in value.uv {
            expected.extend_from_slice(&coordinate.to_ne_bytes());
        }
        expected.extend_from_slice(&value.color.to_ne_bytes());
        for content in value.content_type_with_srgb {
            expected.extend_from_slice(&content.to_ne_bytes());
        }
        expected.extend_from_slice(&value.depth.to_bits().to_ne_bytes());
        expected
    }

    #[test]
    fn gpu_layout_offsets_and_sizes_remain_exact() {
        assert_eq!(size_of::<GlyphToRender>(), 28);
        assert_eq!(offset_of!(GlyphToRender, pos), 0);
        assert_eq!(offset_of!(GlyphToRender, dim), 8);
        assert_eq!(offset_of!(GlyphToRender, uv), 12);
        assert_eq!(offset_of!(GlyphToRender, color), 16);
        assert_eq!(offset_of!(GlyphToRender, content_type_with_srgb), 20);
        assert_eq!(offset_of!(GlyphToRender, depth), 24);
        assert_eq!(size_of::<Resolution>(), 8);
        assert_eq!(size_of::<Params>(), 16);
        assert_eq!(offset_of!(Params, screen_resolution), 0);
        assert_eq!(offset_of!(Params, _pad), 8);
    }

    #[test]
    fn glyph_encoding_preserves_native_integer_and_float_bits() {
        for depth_bits in [0x8000_0000, 0x7fc0_1234, 0x3f80_0000] {
            let value = glyph(depth_bits);
            let actual = bytemuck::bytes_of(&value);
            assert_eq!(actual, expected_glyph(&value));
            assert_eq!(actual.as_ptr(), std::ptr::from_ref(&value).cast::<u8>());
        }
    }

    #[test]
    fn glyph_slice_handles_empty_and_multiple_records_without_copying() {
        let empty: &[GlyphToRender] = &[];
        assert_eq!(bytemuck::cast_slice::<GlyphToRender, u8>(empty), &[]);
        let records = [glyph(0x8000_0000), glyph(0x7fc0_1234)];
        let expected = [expected_glyph(&records[0]), expected_glyph(&records[1])].concat();
        let actual = bytemuck::cast_slice::<GlyphToRender, u8>(&records);
        assert_eq!(actual.len(), 56);
        assert_eq!(actual, expected);
        assert_eq!(actual.as_ptr(), records.as_ptr().cast::<u8>());
    }

    #[test]
    fn uniform_encoding_preserves_resolution_and_explicit_padding() {
        let value = Params {
            screen_resolution: Resolution {
                width: 640,
                height: 480,
            },
            _pad: [0x0102_0304, 0xfedc_ba98],
        };
        let expected = [640_u32, 480, 0x0102_0304, 0xfedc_ba98]
            .into_iter()
            .flat_map(u32::to_ne_bytes)
            .collect::<Vec<_>>();
        let actual = bytemuck::bytes_of(&value);
        assert_eq!(actual, expected);
        assert_eq!(actual.as_ptr(), std::ptr::from_ref(&value).cast::<u8>());
    }
}

/// Controls the visible area of the text. Any text outside of the visible area will be clipped.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct TextBounds {
    /// The position of the left edge of the visible area.
    pub left: i32,
    /// The position of the top edge of the visible area.
    pub top: i32,
    /// The position of the right edge of the visible area.
    pub right: i32,
    /// The position of the bottom edge of the visible area.
    pub bottom: i32,
}

/// The default visible area doesn't clip any text.
impl Default for TextBounds {
    fn default() -> Self {
        Self {
            left: i32::MIN,
            top: i32::MIN,
            right: i32::MAX,
            bottom: i32::MAX,
        }
    }
}

/// A text area containing text to be rendered along with its overflow behavior.
#[derive(Clone)]
pub struct TextArea<'a> {
    /// The buffer containing the text to be rendered.
    pub buffer: &'a Buffer,
    /// The left edge of the buffer.
    pub left: f32,
    /// The top edge of the buffer.
    pub top: f32,
    /// The scaling to apply to the buffer.
    pub scale: f32,
    /// The visible bounds of the text area. This is used to clip the text and doesn't have to
    /// match the `left` and `top` values.
    pub bounds: TextBounds,
    // The default color of the text area.
    pub default_color: Color,
}
