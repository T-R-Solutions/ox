//! Public PNG boundary: independent fixture, bundled assets and invalid streams.
use image::{DynamicImage, ImageBuffer, ImageFormat};
use std::io::Cursor;

// Generated with Python stdlib zlib/struct, independent of image-rs and PNG's encoder.
const FIXTURE: &[u8] = &[
    137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82, 0, 0, 0, 2, 0, 0, 0, 2, 8, 6, 0,
    0, 0, 114, 182, 13, 36, 0, 0, 0, 22, 73, 68, 65, 84, 120, 156, 99, 248, 207, 192, 240, 31, 8,
    27, 24, 64, 180, 160, 146, 241, 127, 0, 55, 240, 5, 226, 186, 166, 239, 61, 0, 0, 0, 0, 73, 69,
    78, 68, 174, 66, 96, 130,
];
const PIXELS: [u8; 16] = [
    255, 0, 0, 255, 0, 255, 0, 128, 0, 0, 255, 0, 17, 34, 51, 255,
];

#[test]
fn independent_png_decodes_exact_rgba() {
    let decoded = image::load_from_memory_with_format(FIXTURE, ImageFormat::Png)
        .unwrap()
        .to_rgba8();
    assert_eq!(decoded.dimensions(), (2, 2));
    assert_eq!(decoded.as_raw(), &PIXELS);
}

#[test]
fn png_roundtrip_preserves_color_and_alpha() {
    let original = ImageBuffer::from_raw(2, 2, PIXELS.to_vec()).unwrap();
    let mut encoded = Cursor::new(Vec::new());
    DynamicImage::ImageRgba8(original)
        .write_to(&mut encoded, ImageFormat::Png)
        .unwrap();
    let decoded = image::load_from_memory_with_format(encoded.get_ref(), ImageFormat::Png)
        .unwrap()
        .to_rgba8();
    assert_eq!(decoded.dimensions(), (2, 2));
    assert_eq!(decoded.as_raw(), &PIXELS);
}

#[test]
fn png_rejects_truncated_and_corrupted_data() {
    assert!(image::load_from_memory_with_format(&FIXTURE[..48], ImageFormat::Png).is_err());
    let mut corrupted = FIXTURE.to_vec();
    // IDAT begins at byte 41; corrupt its compressed payload.
    corrupted[43] ^= 0x80;
    assert!(image::load_from_memory_with_format(&corrupted, ImageFormat::Png).is_err());
    let mut bad_crc = FIXTURE.to_vec();
    // IDAT CRC starts at byte 63; compressed bytes remain intact.
    bad_crc[63] ^= 0x80;
    assert!(image::load_from_memory_with_format(&bad_crc, ImageFormat::Png).is_err());
}

#[test]
fn bundled_identity_pngs_decode_with_expected_dimensions() {
    for (bytes, dimensions) in [
        (
            include_bytes!("../assets/identity/logo-branco.png").as_slice(),
            (960, 300),
        ),
        (
            include_bytes!("../assets/identity/logo-escuro.png").as_slice(),
            (960, 300),
        ),
        (
            include_bytes!("../assets/identity/mascote-ox.png").as_slice(),
            (1065, 1477),
        ),
    ] {
        let decoded = image::load_from_memory_with_format(bytes, ImageFormat::Png)
            .unwrap()
            .to_rgba8();
        assert_eq!(decoded.dimensions(), dimensions);
        assert!(decoded.pixels().any(|pixel| pixel[3] != 0));
    }
}
