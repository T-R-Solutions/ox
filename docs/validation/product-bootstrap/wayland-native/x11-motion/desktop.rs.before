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
    let mut app = App(Command::new(env!("CARGO_BIN_EXE_ox"))
        .env_remove("WAYLAND_DISPLAY")
        .spawn()?);
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
    conn.warp_pointer(x11rb::NONE, window, 0, 0, 0, 0, x, y)?
        .check()?;
    conn.flush()?;
    thread::sleep(Duration::from_millis(80));
    let actual = conn.query_pointer(window)?.reply()?;
    eprintln!(
        "pointer target=({x},{y}), actual=({},{}), same_screen={}",
        actual.win_x, actual.win_y, actual.same_screen
    );
    if actual.win_x != x || actual.win_y != y {
        conn.warp_pointer(
            x11rb::NONE,
            root,
            0,
            0,
            0,
            0,
            pointer.root_x,
            pointer.root_y,
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
    conn.warp_pointer(
        x11rb::NONE,
        root,
        0,
        0,
        0,
        0,
        pointer.root_x,
        pointer.root_y,
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
#[test]
#[ignore = "requires an X11 graphical session; explicit desktop acceptance run"]
fn real_window_toggle_and_exit_button() -> Result {
    let (mut app, conn, window) = launch()?;
    wait_until(|| Ok(title(&conn, window)? == "Ox — Fundação"))?;
    // Allow the first compositor frame to arrive; assertions below await state changes.
    thread::sleep(Duration::from_millis(500));
    eprintln!(
        "window found {window}, initial title {}",
        title(&conn, window)?
    );
    let before = capture(&conn, window, "collapsed")?;
    click(&conn, window, 80, 130)?;
    wait_until(|| Ok(title(&conn, window)?.contains("detalhes")))?;
    thread::sleep(Duration::from_millis(300));
    eprintln!("expanded observed");
    let after = capture(&conn, window, "expanded")?;
    assert_ne!(before, after, "interaction must change rendered pixels");
    click(&conn, window, 80, 130)?;
    wait_until(|| Ok(title(&conn, window)? == "Ox — Fundação"))?;
    eprintln!("collapse observed");
    thread::sleep(Duration::from_millis(300));
    eprintln!("collapsed again; clicking Sair");
    click(&conn, window, 45, 175)?;
    successful_exit(&mut app)?;
    eprintln!("Observed window, expanded/collapsed title and pixels, Sair exit=0");
    Ok(())
}
#[test]
#[ignore = "requires an X11 graphical session; explicit desktop acceptance run"]
fn native_close_returns_success() -> Result {
    let (mut app, conn, window) = launch()?;
    let protocols = conn.intern_atom(false, b"WM_PROTOCOLS")?.reply()?.atom;
    let delete = conn.intern_atom(false, b"WM_DELETE_WINDOW")?.reply()?.atom;
    conn.send_event(
        false,
        window,
        EventMask::NO_EVENT,
        ClientMessageEvent::new(32, window, protocols, [delete, 0, 0, 0, 0]),
    )?
    .check()?;
    conn.flush()?;
    successful_exit(&mut app)?;
    eprintln!("Observed native WM_DELETE_WINDOW exit=0");
    Ok(())
}
