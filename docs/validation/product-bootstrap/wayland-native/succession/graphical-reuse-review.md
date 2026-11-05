# Graphical evidence reuse

Actual application binary, app/ui production sources, manifest, lockfile and
toolchain are byte-identical to both manual Wayland executions. The comparison
also reports changed desktop.rs test source: it is an X11-only harness and was
not executed by either manual Wayland runner. Its correction therefore does not
invalidate human observations of the unchanged binary. Current desktop.rs is
byte-identical to accepted-inputs/application/crates/ox-app/tests/desktop.rs,
the version used by the successful rootful Xwayland run. No graphical rerun is
needed for the subsequent independent library changes. Main-session XTEST
failures remain historical failures, not corrected by this reuse.
