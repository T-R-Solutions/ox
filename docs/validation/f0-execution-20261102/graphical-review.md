# Observed graphical acceptance and remaining limits

Production application sources remain the versions bound in the final input
manifest. Separate uninstrumented X11 tests: six passed at scale 1; visual/resize/
keyboard-scroll corpus passed separately at 1.5 and 2. The common Rust suite
reports six explicitly ignored graphics, not six automatic passes.

Inspected captured frames: keyboard-focus shows the black focus border; the
640×480 PageDown frame exposes status and volatile-history warning with the focused
control visible; held-cancellation frame shows INCONCLUSIVE, a Cancelled observation,
retained inputs and history. The default screen text identifies trusted local
fixtures and absence of sandbox/remote agents/persisted history. Shared Light theme,
button styling, spacing and wrapped rows were inspected. Selected contrast ratios
are in contrast.json: 4.607 white/primary, 7.005 placeholder/white, 4.559 black focus/
primary, 21 black/white. These selected checks are not full WCAG conformance or an
assistive-technology claim. Different rendered dimensions were intentionally
compared after scaling; the earlier unscaled observation-region failure is retained.

Instrumented coverage: five tests passed and held-verification details observation
timed out; an unchanged targeted repeat passed. Separate frame-instrumented copy:
scale 1 failed final keyboard exit after measurements; 1.5/2 passed. A subsequent
copy with update-message diagnostics and all auxiliary binaries built passed all
six. The initial diagnostic copy had missing auxiliary executables, explicitly
reported as fixture preparation failure, not product failure. These repetitions do
not establish the cause of earlier intermittency or erase it.

Additional copied-oracle keyboard case successfully observes Enter and Space
Toggle messages. Shift+Tab injection did not produce a backward focus event.
The next run holds the mapped Shift for 100 ms and queries X11's modifier mask:
the server reports Shift absent, so the assertion stops before injecting Tab.
This discriminates a failed test-input precondition from a product navigation bug.
Logs and exact copied test source are in gui-diagnostic-1-keyboard and
 gui-diagnostic-1-keyboard-held. No Xvfb, Xephyr, weston, cage or ydotool executable
was available on PATH. A compositor/session that delivers actual held modifiers,
or a correlated native human observation, is needed to prove Shift+Tab. No global
installation or whole-session input takeover was performed.

Native Wayland: first unidentified process timed out and was terminated; maintainer
reported it might have been another window. Identified F0-20261102-B (PID 1637135)
exited 0. Maintainer reported completing all steps, but /tmp/oxf0native2 contained
zero task artifacts; follow-up actual-workspace answer was “não lembro”. Window
closure is APPROVED; the task/verification/cancel/focus journey is INCONCLUSIVE.
Human answers and conflicting machine observations are both retained.

Resume with an identified native window, a recorded validated workspace path,
before/after task manifests plus APPROVED/REJECTED observations, owned child PID/
exit and native close. Record held-modifier/focus input and named scale/size cases.
Use an exclusive test session or a reliable input mechanism before accepting the
intermittent scenarios. Maintainer supplies the session/actual interaction; executor
collects and reconciles the evidence. No replay of unaffected backend tests is needed.
