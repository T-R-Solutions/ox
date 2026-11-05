//! Real X11 integration. Run explicitly with --ignored on a graphical Linux host.
#![forbid(unsafe_code)]
use std::{
    process::{Child, Command},
    thread,
    time::{Duration, Instant},
};
use x11rb::{connection::Connection, protocol::xproto::*, rust_connection::RustConnection};

type Result<T = ()> = std::result::Result<T, Box<dyn std::error::Error>>;
struct App(Child);
impl Drop for App {
    fn drop(&mut self) {
        let _ = self.0.kill();
        let _ = self.0.wait();
    }
}
fn wait_until(mut check: impl FnMut() -> Result<bool>) -> Result {
    let deadline = Instant::now() + Duration::from_secs(15);
    while Instant::now() < deadline {
        if check()? {
            return Ok(());
        }
        thread::sleep(Duration::from_millis(50));
    }
    Err("desktop observation timed out after 15s".into())
}
fn find(conn: &RustConnection, root: Window, pid_atom: Atom, pid: u32) -> Result<Option<Window>> {
    let property = conn
        .get_property(false, root, pid_atom, AtomEnum::CARDINAL, 0, 1)?
        .reply()?;
    if property.value32().and_then(|mut v| v.next()) == Some(pid) {
        return Ok(Some(root));
    }
    for child in conn.query_tree(root)?.reply()?.children {
        if let Some(window) = find(conn, child, pid_atom, pid)? {
            return Ok(Some(window));
        }
    }
    Ok(None)
}
fn launch() -> Result<(App, RustConnection, Window)> {
    let (conn, screen) = x11rb::connect(None)?;
    let root = conn.setup().roots[screen].root;
    let atom = conn.intern_atom(false, b"_NET_WM_PID")?.reply()?.atom;
    let mut app = App(
        Command::new(std::env::var("OX_GUI_CONSUMER").expect("consumer executable"))
            .env_remove("WAYLAND_DISPLAY")
            .current_dir(std::env::temp_dir())
            .spawn()?,
    );
    let mut window = None;
    wait_until(|| {
        if let Some(status) = app.0.try_wait()? {
            return Err(format!("app exited before window: {status}").into());
        }
        window = find(&conn, root, atom, app.0.id())?;
        Ok(window.is_some())
    })?;
    Ok((app, conn, window.ok_or("missing window")?))
}
fn title(conn: &RustConnection, window: Window) -> Result<String> {
    let atom = conn.intern_atom(false, b"_NET_WM_NAME")?.reply()?.atom;
    let value = conn
        .get_property(false, window, atom, AtomEnum::ANY, 0, 1024)?
        .reply()?
        .value;
    Ok(String::from_utf8(value)?)
}
fn click(conn: &RustConnection, window: Window, x: i16, y: i16) -> Result {
    use x11rb::protocol::xtest::ConnectionExt as _;
    let root = conn.get_geometry(window)?.reply()?.root;
    let pointer = conn.query_pointer(root)?.reply()?;
    conn.set_input_focus(InputFocus::POINTER_ROOT, window, x11rb::CURRENT_TIME)?
        .check()?;
    conn.configure_window(
        window,
        &ConfigureWindowAux::new().stack_mode(StackMode::ABOVE),
    )?
    .check()?;
    // Use the same XTEST input path for motion and clicks under XWayland.
    let target = conn.translate_coordinates(window, root, x, y)?.reply()?;
    let placement = wait_until(|| {
        conn.xtest_fake_input(
            MOTION_NOTIFY_EVENT,
            0,
            0,
            root,
            target.dst_x,
            target.dst_y,
            0,
        )?
        .check()?;
        conn.flush()?;
        thread::sleep(Duration::from_millis(80));
        let actual = conn.query_pointer(window)?.reply()?;
        Ok(actual.win_x == x && actual.win_y == y)
    });
    let actual = conn.query_pointer(window)?.reply()?;
    eprintln!(
        "pointer target=({x},{y}), actual=({},{}), same_screen={}",
        actual.win_x, actual.win_y, actual.same_screen
    );
    if placement.is_err() || actual.win_x != x || actual.win_y != y {
        conn.xtest_fake_input(
            MOTION_NOTIFY_EVENT,
            0,
            0,
            root,
            pointer.root_x,
            pointer.root_y,
            0,
        )?
        .check()?;
        return Err(
            "graphical session did not honor pointer placement; cannot validate button input"
                .into(),
        );
    }
    conn.xtest_fake_input(BUTTON_PRESS_EVENT, 1, 0, x11rb::NONE, 0, 0, 0)?
        .check()?;
    conn.flush()?;
    thread::sleep(Duration::from_millis(100));
    conn.xtest_fake_input(BUTTON_RELEASE_EVENT, 1, 0, x11rb::NONE, 0, 0, 0)?
        .check()?;
    conn.flush()?;
    thread::sleep(Duration::from_millis(80));
    conn.xtest_fake_input(
        MOTION_NOTIFY_EVENT,
        0,
        0,
        root,
        pointer.root_x,
        pointer.root_y,
        0,
    )?
    .check()?;
    conn.flush()?;
    Ok(())
}
fn capture(conn: &RustConnection, window: Window, name: &str) -> Result<Vec<u8>> {
    let geometry = conn.get_geometry(window)?.reply()?;
    let reply = conn
        .get_image(
            ImageFormat::Z_PIXMAP,
            window,
            0,
            0,
            geometry.width,
            geometry.height,
            u32::MAX,
        )?
        .reply()?;
    if let Ok(directory) = std::env::var("OX_DESKTOP_CAPTURE_DIR") {
        // This harness supports the observed little-endian 24-bit X11 framebuffer only.
        if reply.depth != 24
            || conn.setup().image_byte_order != ImageOrder::LSB_FIRST
            || reply.data.len() != usize::from(geometry.width) * usize::from(geometry.height) * 4
        {
            return Err("unsupported screenshot pixel layout".into());
        }
        let mut ppm = format!("P6\n{} {}\n255\n", geometry.width, geometry.height).into_bytes();
        for pixel in reply.data.as_chunks::<4>().0 {
            ppm.extend_from_slice(&[pixel[2], pixel[1], pixel[0]]);
        }
        std::fs::write(
            std::path::Path::new(&directory).join(format!("{name}.ppm")),
            ppm,
        )?;
    }
    Ok(reply.data)
}
fn successful_exit(app: &mut App) -> Result {
    wait_until(|| match app.0.try_wait()? {
        Some(status) if status.success() => Ok(true),
        Some(status) => Err(format!("shutdown failed: {status}").into()),
        None => Ok(false),
    })
}
fn type_ascii(conn: &RustConnection, value: &str) -> Result {
    use x11rb::protocol::xtest::ConnectionExt as _;
    let setup = conn.setup();
    let mapping = conn
        .get_keyboard_mapping(setup.min_keycode, setup.max_keycode - setup.min_keycode + 1)?
        .reply()?;
    for byte in value.bytes() {
        let index = mapping
            .keysyms
            .chunks(usize::from(mapping.keysyms_per_keycode))
            .position(|symbols| symbols.first() == Some(&u32::from(byte)))
            .ok_or("ASCII key unavailable in unshifted mapping")?;
        let key = setup.min_keycode + u8::try_from(index)?;
        conn.xtest_fake_input(KEY_PRESS_EVENT, key, 0, x11rb::NONE, 0, 0, 0)?
            .check()?;
        conn.xtest_fake_input(KEY_RELEASE_EVENT, key, 0, x11rb::NONE, 0, 0, 0)?
            .check()?;
        conn.flush()?;
        thread::sleep(Duration::from_millis(15));
    }
    Ok(())
}
fn metric(conn: &RustConnection, w: Window, key: &str) -> Result<String> {
    let value = title(conn, w)?;
    Ok(value
        .split('|')
        .find_map(|p| p.strip_prefix(&format!("{key}=")))
        .ok_or("missing metric")?
        .into())
}
fn number(conn: &RustConnection, w: Window, key: &str) -> Result<u64> {
    Ok(metric(conn, w, key)?.parse()?)
}
fn resize(conn: &RustConnection, w: Window, width: u32, height: u32) -> Result {
    conn.configure_window(w, &ConfigureWindowAux::new().width(width).height(height))?
        .check()?;
    conn.flush()?;
    wait_until(|| {
        let g = conn.get_geometry(w)?.reply()?;
        Ok(u32::from(g.width) == width && u32::from(g.height) == height)
    })?;
    thread::sleep(Duration::from_millis(200));
    Ok(())
}
#[test]
fn iced_four_criteria() -> Result {
    let (mut app, conn, w) = launch()?;
    thread::sleep(Duration::from_millis(500));
    conn.set_input_focus(InputFocus::POINTER_ROOT, w, x11rb::CURRENT_TIME)?
        .check()?;
    conn.flush()?;
    wait_until(|| Ok(number(&conn, w, "ticks")? > 2))?;
    // Type into the actual focused widget, then verify collapse/expand routing and retained content.
    click(&conn, w, 80, 105)?;
    type_ascii(&conn, "retained")?;
    wait_until(|| Ok(metric(&conn, w, "detail")? == "retained"))?;
    click(&conn, w, 30, 22)?;
    wait_until(|| Ok(metric(&conn, w, "busy")? == "1"))?;
    let before = number(&conn, w, "ticks")?;
    click(&conn, w, 83, 22)?;
    wait_until(|| Ok(metric(&conn, w, "pane")? == "0" && metric(&conn, w, "focus")? == "1"))?;
    type_ascii(&conn, "cmd")?;
    wait_until(|| Ok(metric(&conn, w, "command")? == "cmd"))?;
    assert_eq!(metric(&conn, w, "busy")?, "1");
    assert!(number(&conn, w, "ticks")? > before);
    click(&conn, w, 83, 22)?;
    wait_until(|| Ok(metric(&conn, w, "pane")? == "1" && metric(&conn, w, "focus")? == "1"))?;
    assert_eq!(metric(&conn, w, "detail")?, "retained");
    type_ascii(&conn, "x")?;
    wait_until(|| Ok(metric(&conn, w, "detail")?.contains('x')))?;
    println!(
        "AC01: UI heartbeat and XTEST pane/typing interactions during 3-second worker; AC02: content retained and actual focus operations observed"
    );
    wait_until(|| Ok(metric(&conn, w, "busy")? == "0"))?;
    for (width, height) in [(240, 180), (1600, 1000)] {
        resize(&conn, w, width, height)?;
        capture(&conn, w, &format!("layout-{width}x{height}"))?;
        let pane = metric(&conn, w, "pane")?;
        click(&conn, w, 83, 22)?;
        wait_until(|| Ok(metric(&conn, w, "pane")? != pane))?;
        click(&conn, w, 30, 22)?;
        wait_until(|| Ok(metric(&conn, w, "busy")? == "1"))?;
        let hidden = number(&conn, w, "layouts")?;
        thread::sleep(Duration::from_millis(300));
        assert_eq!(number(&conn, w, "layouts")?, hidden);
        click(&conn, w, 143, 22)?;
        wait_until(|| Ok(number(&conn, w, "layouts")? > hidden + 3))?;
        click(&conn, w, 143, 22)?;
        wait_until(|| Ok(metric(&conn, w, "graph")? == "0"))?;
        let stopped = number(&conn, w, "layouts")?;
        thread::sleep(Duration::from_millis(300));
        assert_eq!(number(&conn, w, "layouts")?, stopped);
        println!(
            "AC03: actual geometry {width}x{height}, top actions usable; AC04: hidden={hidden}, visible increased, hidden stopped={stopped}"
        );
        wait_until(|| Ok(metric(&conn, w, "busy")? == "0"))?;
    }
    resize(&conn, w, 240, 180)?;
    click(&conn, w, 198, 22)?;
    successful_exit(&mut app)?;
    println!("Quit action observed at minimum size; exit=0");
    Ok(())
}
