# Bootstrap reconciliation after local task UI

AC-01/07: Current Cargo metadata has the same 16 workspace members and only two new
local edges from ox-ui to existing ox-agent and ox-verification. Build/check succeeds;
Desktop presentation is separated from Controller and the reused domain libraries.
AC-02/06: Native Wayland observation plus three explicit X11 tests preserve launch,
rendered details, button exit and native close. Regular tests/discovery also pass.
AC-03: ox main still delegates to ox_app::run, then ox_ui::run.
AC-04/05: Existing crate roots forbid unsafe; both new fixture binaries also forbid it.
The added controller is an external module file. No mod.rs or first-party unsafe added.
AC-08: Existing identity contracts remain; Controller's session nonce/task/attempt and
Runtime's process-session namespace are explicitly mapped, with no global UUID claim.
AC-09: New content-bound records preserve older envelopes; no prior execution is rehashed.
AC-10/12: New independent governance export/checks preserve recovery, test coverage,
Git exclusion and the product/governance boundary. New feature and its records excluded.
AC-11: NOT APPLICABLE for the already-superseded absence-of-IPC clause; accepted local
Plugin Host predecessor remains independent. The supersession was authorized before
this UI delivery and is not a waived graphical gate.
AC-13: Local fixture controls are now actually implemented under explicit authorization.
UI does not advertise general/remote agents, sandbox or persistent history. The earlier
shell-only wording is retained as historical scope and explicitly succeeded in spec/plan.
This accepts current bounded bootstrap obligations, not the entire F0 roadmap.
