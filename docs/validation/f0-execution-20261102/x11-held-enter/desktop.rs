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
    launch_binary(std::path::Path::new(env!("CARGO_BIN_EXE_ox")))
}
fn launch_binary(binary: &std::path::Path) -> Result<(App, RustConnection, Window)> {
    let (conn, screen) = x11rb::connect(None)?;
    let root = conn.setup().roots[screen].root;
    let atom = conn.intern_atom(false, b"_NET_WM_PID")?.reply()?.atom;
    let mut app = App(Command::new(binary)
        .env_remove("WAYLAND_DISPLAY")
        .current_dir(std::env::temp_dir())
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
    capture(&conn, window, "recollapsed")?;
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

fn key(conn: &RustConnection, keysym: u32) -> Result {
    use x11rb::protocol::xtest::ConnectionExt as _;
    let setup = conn.setup();
    let mapping = conn
        .get_keyboard_mapping(setup.min_keycode, setup.max_keycode - setup.min_keycode + 1)?
        .reply()?;
    let index = mapping
        .keysyms
        .chunks(usize::from(mapping.keysyms_per_keycode))
        .position(|symbols| symbols.first() == Some(&keysym))
        .ok_or("keysym unavailable")?;
    let code = setup.min_keycode + u8::try_from(index)?;
    for event in [KEY_PRESS_EVENT, KEY_RELEASE_EVENT] {
        conn.xtest_fake_input(event, code, 0, x11rb::NONE, 0, 0, 0)?
            .check()?;
    }
    conn.flush()?;
    Ok(())
}

#[test]
#[ignore = "requires dedicated X11 keyboard input and visual focus inspection"]
fn keyboard_focus_activation_and_exit() -> Result {
    let (mut app, conn, window) = launch()?;
    wait_until(
        || Ok(conn.get_window_attributes(window)?.reply()?.map_state == MapState::VIEWABLE),
    )?;
    conn.set_input_focus(InputFocus::POINTER_ROOT, window, x11rb::CURRENT_TIME)?
        .check()?;
    conn.flush()?;
    thread::sleep(Duration::from_millis(300));
    key(&conn, 0xff09)?; // Tab: first enabled control, details.
    thread::sleep(Duration::from_millis(100));
    capture(&conn, window, "keyboard-focus")?;
    key(&conn, 0xff0d)?; // Return activates focused button.
    wait_until(|| Ok(title(&conn, window)?.contains("detalhes")))?;
    key(&conn, 0xff09)?; // Exit follows details in visual order.
    key(&conn, 0xff0d)?;
    successful_exit(&mut app)?;
    Ok(())
}

#[test]
#[ignore = "requires dedicated X11; measures input-to-observed-pixel response, not compositor presentation"]
fn visual_response_and_window_matrix() -> Result {
    let scale: f32 = std::env::var("WINIT_X11_SCALE_FACTOR")
        .ok()
        .and_then(|s| s.parse().ok())
        .unwrap_or(1.0);
    let (mut app, conn, window) = launch()?;
    wait_until(
        || Ok(conn.get_window_attributes(window)?.reply()?.map_state == MapState::VIEWABLE),
    )?;
    conn.set_input_focus(InputFocus::POINTER_ROOT, window, x11rb::CURRENT_TIME)?
        .check()?;
    conn.flush()?;
    thread::sleep(Duration::from_millis(300));
    key(&conn, 0xff09)?;
    thread::sleep(Duration::from_millis(100));
    let pixels = || -> Result<Vec<u8>> {
        Ok(conn
            .get_image(
                ImageFormat::Z_PIXMAP,
                window,
                0,
                0,
                (400.0 * scale) as u16,
                (200.0 * scale) as u16,
                u32::MAX,
            )?
            .reply()?
            .data)
    };
    for iteration in 0..23 {
        let before = pixels()?;
        let start = Instant::now();
        key(&conn, 0xff0d)?;
        loop {
            if pixels()? != before {
                break;
            }
            if start.elapsed() > Duration::from_secs(2) {
                return Err("no rendered response".into());
            }
            thread::sleep(Duration::from_millis(2));
        }
        if iteration >= 3 {
            eprintln!(
                "VISUAL_RESPONSE_MS={:.6}",
                start.elapsed().as_secs_f64() * 1000.
            );
        }
        // Ensure each subsequent sample begins after the previous event settles.
        thread::sleep(Duration::from_millis(30));
    }
    for (logical_width, logical_height) in [(640, 480), (900, 700)] {
        let width = (logical_width as f32 * scale) as u32;
        let height = (logical_height as f32 * scale) as u32;
        conn.configure_window(
            window,
            &ConfigureWindowAux::new().width(width).height(height),
        )?
        .check()?;
        conn.flush()?;
        wait_until(|| {
            let g = conn.get_geometry(window)?.reply()?;
            Ok(u32::from(g.width) == width && u32::from(g.height) == height)
        })?;
        thread::sleep(Duration::from_millis(200));
        capture(&conn, window, &format!("size-{width}-{height}"))?;
    }
    eprintln!(
        "GUI_PROC_STATUS_BEGIN\n{}GUI_PROC_STATUS_END",
        std::fs::read_to_string(format!("/proc/{}/status", app.0.id()))?
    );
    let idle_before = std::fs::read_to_string(format!("/proc/{}/stat", app.0.id()))?;
    let idle_start = Instant::now();
    thread::sleep(Duration::from_secs(1));
    let idle_after = std::fs::read_to_string(format!("/proc/{}/stat", app.0.id()))?;
    eprintln!(
        "GUI_IDLE_SECONDS={}\nGUI_STAT_BEFORE={}\nGUI_STAT_AFTER={}",
        idle_start.elapsed().as_secs_f64(),
        idle_before.trim(),
        idle_after.trim()
    );
    key(&conn, 0xff09)?;
    key(&conn, 0xff0d)?;
    successful_exit(&mut app)?;
    Ok(())
}

#[test]
#[ignore = "requires dedicated X11 and built held-task-oracle fixture"]
fn cancel_verification_observes_oracle_exit_in_ui() -> Result {
    let root = std::env::temp_dir().join(format!("oxheld{}", std::process::id()));
    std::fs::create_dir(&root)?;
    let bins = root.join("bins");
    std::fs::create_dir(&bins)?;
    let built = std::path::Path::new(env!("CARGO_BIN_EXE_ox"))
        .parent()
        .ok_or("bin parent")?;
    for (source, target) in [
        ("ox", "ox"),
        ("local-task", "local-task"),
        ("held-task-oracle", "task-oracle"),
    ] {
        std::fs::copy(built.join(source), bins.join(target))?;
    }
    let workspace = root.clone();
    std::fs::write(workspace.join("sentinel"), b"preserve")?;
    let (mut app, conn, window) = launch_binary(&bins.join("ox"))?;
    thread::sleep(Duration::from_millis(400));
    click(&conn, window, 300, 225)?;
    type_ascii(
        &conn,
        workspace
            .file_name()
            .and_then(|p| p.to_str())
            .ok_or("path")?,
    )?;
    key(&conn, 0xff0d)?;
    thread::sleep(Duration::from_millis(300));
    capture(&conn, window, "held-workspace-valid")?;
    click(&conn, window, 80, 322)?;
    let mut attempt = None;
    wait_until(|| {
        attempt = std::fs::read_dir(&workspace)?
            .filter_map(|p| p.ok())
            .map(|p| p.path())
            .find(|p| p.join("result.txt").exists());
        Ok(attempt.is_some())
    })?;
    let attempt = attempt.ok_or("attempt")?;
    thread::sleep(Duration::from_millis(100));
    click(&conn, window, 180, 368)?;
    let mut pid = None;
    wait_until(|| {
        pid = std::fs::read_to_string(attempt.join("oracle-ready"))
            .ok()
            .and_then(|s| s.parse::<u32>().ok());
        Ok(pid.is_some())
    })?;
    let pid = pid.ok_or("oracle pid")?;
    // Toggle while verification is held: visible change proves the UI event loop progresses.
    click(&conn, window, 80, 130)?;
    wait_until(|| Ok(title(&conn, window)?.contains("detalhes")))?;
    capture(&conn, window, "held-verification-responsive")?;
    click(&conn, window, 80, 130)?;
    wait_until(|| Ok(!title(&conn, window)?.contains("detalhes")))?;
    click(&conn, window, 50, 368)?;
    wait_until(|| Ok(!std::path::Path::new(&format!("/proc/{pid}")).exists()))?;
    thread::sleep(Duration::from_millis(100));
    capture(&conn, window, "cancelled-verification")?;
    assert_eq!(std::fs::read(workspace.join("sentinel"))?, b"preserve");
    // A second held verification exercises close while verification is active.
    std::fs::remove_file(attempt.join("oracle-ready"))?;
    click(&conn, window, 180, 368)?;
    let mut second = None;
    wait_until(|| {
        second = std::fs::read_to_string(attempt.join("oracle-ready"))
            .ok()
            .and_then(|s| s.parse::<u32>().ok());
        Ok(second.is_some())
    })?;
    let second = second.ok_or("second pid")?;
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
    assert!(!std::path::Path::new(&format!("/proc/{second}")).exists());
    Ok(())
}
#[test]
#[ignore = "requires dedicated X11 input and visual review of captured frames"]
fn local_task_rendered_flow() -> Result {
    let directory = std::env::temp_dir().join(format!(
        "oxuitest{}",
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)?
            .as_nanos()
    ));
    std::fs::create_dir(&directory)?;
    std::fs::write(directory.join("sentinel"), b"user content")?;
    let (mut app, conn, window) = launch()?;
    thread::sleep(Duration::from_millis(500));
    click(&conn, window, 300, 225)?;
    type_ascii(
        &conn,
        directory
            .file_name()
            .and_then(|name| name.to_str())
            .ok_or("non UTF8 fixture")?,
    )?;
    click(&conn, window, 100, 275)?;
    thread::sleep(Duration::from_millis(300));
    capture(&conn, window, "workspace-valid")?;
    click(&conn, window, 80, 322)?;
    let mut attempt = None;
    wait_until(|| {
        attempt = std::fs::read_dir(&directory)?
            .filter_map(|e| e.ok())
            .map(|e| e.path())
            .find(|p| p.join("result.txt").is_file());
        Ok(attempt.is_some())
    })?;
    let attempt = attempt.ok_or("missing task directory")?;
    let request = std::fs::read(attempt.join("request.txt"))?;
    let mut expected = request.clone();
    expected.extend_from_slice(b"result=42\n");
    assert_eq!(std::fs::read(attempt.join("result.txt"))?, expected);
    thread::sleep(Duration::from_millis(100));
    click(&conn, window, 180, 368)?;
    thread::sleep(Duration::from_millis(500));
    capture(&conn, window, "correct-verdict")?;
    std::fs::write(attempt.join("result.txt"), b"incorrect controlled result")?;
    click(&conn, window, 300, 368)?;
    thread::sleep(Duration::from_millis(300));
    capture(&conn, window, "stale-verdict")?;
    click(&conn, window, 180, 368)?;
    thread::sleep(Duration::from_millis(300));
    capture(&conn, window, "incorrect-verdict")?;
    click(&conn, window, 363, 322)?;
    thread::sleep(Duration::from_millis(200));
    click(&conn, window, 80, 130)?;
    wait_until(|| Ok(title(&conn, window)?.contains("detalhes")))?;
    capture(&conn, window, "responsive-during-task")?;
    // Native close during active execution must wait for supervised termination.
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
    assert_eq!(std::fs::read(directory.join("sentinel"))?, b"user content");
    eprintln!(
        "Real pointer/keyboard flow and task artifacts observed; verdict text requires captured-frame review. Workspace {}",
        directory.display()
    );
    Ok(())
}
