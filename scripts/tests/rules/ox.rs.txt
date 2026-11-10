use std::process::Command;
fn examples() {
    // ruleid: ox.rust.unsafe-block
    unsafe { action(); }
    // ok: ox.rust.unsafe-block
    { safe_action(); }
    // ruleid: ox.rust.shell-interpreter
    Command::new("sh");
    // ruleid: ox.rust.shell-interpreter
    std::process::Command::new("bash");
    // ok: ox.rust.shell-interpreter
    Command::new("git");
    // ruleid: ox.rust.tls-verification-disabled
    builder.danger_accept_invalid_certs(true);
    // ruleid: ox.rust.tls-verification-disabled
    builder.danger_accept_invalid_hostnames(true);
    // ok: ox.rust.tls-verification-disabled
    builder.danger_accept_invalid_certs(false);
}
// ruleid: ox.rust.unsafe-function
unsafe fn forbidden() {}
// ok: ox.rust.unsafe-function
fn permitted() {}
// ruleid: ox.rust.unsafe-impl
unsafe impl Send for Example {}
// ok: ox.rust.unsafe-impl
impl Example {}
