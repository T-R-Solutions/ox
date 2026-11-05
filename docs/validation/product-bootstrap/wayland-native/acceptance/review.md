# Acceptance review

All 13 bootstrap criteria reexamined after additive D-07/T010 and the
X11 harness-only change. Requirements, application implementations, lockfile,
toolchain and governance implementation are unchanged. The test now uses
XTEST motion with root coordinates and XTEST buttons, preserving title, pixel,
reversal and both exit assertions. Current five Cargo commands pass.

AC-01/04/05/07: structural/dependency observations remain applicable to
unchanged workspace and lockfile; no transitive safety audit inferred.
AC-03/08/11/13: unchanged contracts plus current tests/check. Plugin host
implementation, agents and persistence remain absent at this acceptance point.
AC-02: human visual observation of both native Wayland runs, independently
recorded protocol and successful exits. Both X11 tests also pass in rootful
Xwayland with corrected harness; main GNOME XTEST path remains limited.
AC-06: seven regular tests and both explicitly invoked graphical tests pass;
nine tests discovered. Prior failures preserved, not overwritten.
AC-09: current content bindings, archived prior envelope and current review.
AC-10: current governance and SDD checks, retaining pending unrelated criteria.
AC-12: no distribution code/config change; unchanged boundary review and
historical exclusion tests reused, not a newly generated package claim.

The prior envelope and its input hashes are retained in evidence.json.before.
New records distinguish reruns, human observations and explicit reuse review.
This accepts only bootstrap; no F0 or later slice implementation inferred.
