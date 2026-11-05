# Reproduce the controlled local task flow

From application/: `cargo build --workspace`, then `cargo run -p ox-app --bin ox`.
All three binaries (ox, local-task, task-oracle) must remain in the same build directory.
Select an existing accessible local directory by entering its path and choosing
Validate workspace. Selection is not a sandbox grant. No arbitrary command is accepted.

Run correct creates a new exclusive .ox-task-<session>-<attempt> directory with
request.txt and result.txt. Observed process Success remains UNVERIFIED until
Verify result executes the independent task-oracle. Run incorrect exits successfully
but its result=41 is rejected; the independent oracle requires identity and result=42.
Fail returns Failed; Timeout exceeds the ten-second supervision bound. Cancel requests
termination and waits for the observed child exit. Window close stops admission and
waits for the owned operation; verification finishes under its existing deadline.

After approval, modify only the controlled result.txt in the displayed task directory
and choose Refresh inputs. Current acceptance becomes UNVERIFIED/stale; history remains.
Verify result creates a new observation. Missing result files cannot approve. Existing
workspace files are neither replaced nor recursively cleaned. Keep task directories as
local artifacts; restart begins without acceptance or in-memory history.

No continuous monitoring: status is valid as of the displayed observation time. Use
Refresh inputs after external changes. The engine retains at most 32 observations;
resource-limit errors cannot create approval. History is not durable. Forced application
kill, process descendants, OS confinement and production agents are outside this slice.

Checks: cargo check --workspace; cargo fmt --all -- --check;
cargo clippy --workspace --all-targets -- -D warnings; cargo test --workspace;
cargo test --workspace -- --list. Build fixtures before local_task integration tests.
Unix socket tests require an environment allowing local sockets. Explicit X11 tests
remain separate from Wayland human observation; temporary Xwayland does not establish
repair of the main GNOME XTEST path.
