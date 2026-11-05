# Native Wayland resumption review

Method: inspect current bootstrap spec, traceability, sources, previous envelope
and compare the 83 bound inputs; run exact current Cargo toolchain commands.
Plan D-06 and tasks T008/T009 add validation, without changing any AC or source.

- AC-01/04/05/07: current structural oracle passes, 16 crates, acyclic dependency
  graph, forbid unsafe roots, single lockfile; dependency review reused only for
  unchanged application/lockfile and prior comparison inputs. No full audit.
- AC-03/08/11/13: implementation, contract tests and relevant ADRs unchanged;
  current regular tests/check pass. Binary delegates; identities remain distinct;
  plugin contract is in memory, no IPC/sandbox/runtime implementation is inferred.
- AC-02: INCONCLUSIVE. Native protocol traffic observed, screenshots denied by
  GNOME. No claim of visible rendering, toggle, reversal or either UI close path.
  Probe cleanup exit -15 is not an application crash or successful UI termination.
- AC-06: INCONCLUSIVE. Seven regular tests pass and nine tests discovered; two
  graphical tests ignored, existing X11 toggle failure remains unresolved.
- AC-09: new observations bind current inputs; historical envelopes preserved.
  Scope extension does not retrospectively change prior executions.
- AC-10: rerun current governance checks after explicit dependent invalidation;
  check success proves operation, not approval of pending governance criteria.
- AC-12: no distribution implementation/configuration changed; historical
  product-exclusion test result remains relevant to this unchanged boundary.
  Historical package is not claimed to contain the newly modified project file.

Environment limitation: org.gnome.Shell.Screenshot.ScreenshotWindow and
org.gnome.Shell.Introspect.GetWindows return AccessDenied. Shell Eval is disabled.
No permissions were relaxed, global tool installed or remote provider used.
The Mutter remote-session interface was inspected but no input sent.
No product source repair is justified by this evidence.

Protocol and visual evidence are deliberately distinct. No later slice was
implemented because the requested predecessor acceptance gate is unsatisfied.
