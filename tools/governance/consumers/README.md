# Bounded skill consumers

These executable Rust consumers evaluate the nine library skills under
`sdd/features/skill-consumer-validation`. They do not add production engines to
Ox. The original scenario definitions remain in the corresponding skill features.
Rust 1.99.1, edition 2024, Linux x86_64; first-party unsafe code is prohibited.
Python only orchestrates builds, isolation and graphical observations.

Run the deterministic and process/filesystem scenarios from the repository root:

```sh
python3 tools/governance/consumers/run_base.py /tmp/ox-consumer-report --isolation
```

The report directory must not already exist. This compiles five binaries, runs
16 model tests and seven process/filesystem tests, then four real read attempts
with positive/negative isolation controls. Local Unix/TCP sockets and Bubblewrap
namespaces require the corresponding environment permissions. The receiver binds
only ephemeral loopback. No external publication occurs. Every command, exit,
source hash and executable hash is retained; a failed command stops the runner.
The temporary binaries and fixture directories remain inspectable in /tmp.

The separate graphical consumer links Iced 0.14.0 and x11rb 0.13.2 from the local
application dependency build. Exact compiler, dependency lock/configuration and
rlib identities are recorded in the validation environment manifest. Build with
`rustc +1.99.1 --edition=2024`, `-L dependency=application/target/debug/deps` and
`--extern iced=<observed rlib>` for gui.rs, and `--test --extern
x11rb=<observed rlib>` for gui_tests.rs. Destinations are /tmp/ox-consumer-gui
and /tmp/ox-consumer-gui-tests. Then run:

```sh
python3 tools/governance/consumers/gui_test.py /tmp/ox-gui-report
```

A dedicated nested Xwayland session performs actual XTEST input and captures raw
pixels at 240x180 and 1600x1000. The report directory must be new. Inspect the
screenshots as well as assertions; a reducer test is insufficient for this gate.
This runner requires an authorized local graphical session and exits its server.
The portably exported source package does not contain compiled dependencies.

## Contracts and exclusions

- Models: usage records use a synthetic provider contract where cached tokens
  are a subset of input, integer prices per token and explicit fixed UTC offsets.
  Missing prices remain unknown. This does not verify a commercial provider or
  timezone database/DST behavior. Duplicate identity includes provider and event.
- Context: an explicit synthetic source language (`fn NAME`, `call NAME`,
  `import NAME`, comments), not a Rust parser or functioning LSP client. Changed
  files are reparsed; unchanged bytes reuse parsed declarations. Snapshot identity
  includes generation and exact source bytes. File rename/edit uses real temporary
  files. Same-name/import ambiguity remains syntactic. Starting an absent provider
  yields explicit degradation; a successful executable cannot masquerade as LSP.
- Graph: calls resolve only to uniquely declared local functions in this synthetic
  language. Evidence contains exact bytes, byte range and method. Inference cannot
  be promoted by toggling a flag. All examined edges count against query budgets,
  including nonmatching edges; no production graph/UI performance claim follows.
- Output: preserve raw bytes exclusively, escape terminal controls, prioritize
  known error lines, label fallback and truncation, and carry exit/raw location.
  A byte heuristic is never billing. Grammar is deliberately limited to `ok:` and
  `error:` lines; no arbitrary CLI or incremental streaming parser is accepted.
- Workspace: one transaction per owned fixture, static symlink/traversal rejection,
  exact-byte compare and a lock shared by cooperating writers. The crash case is
  process exit after PREPARED/before rename; recovery retains an unapplied proposal
  after observing a reaped owner. Hostile concurrent directory replacement,
  noncooperating write races, PID reuse recovery and power-loss durability are
  excluded. Polling is a hint; actual reads remain authoritative after lost hints.
- Runtime: a controlled direct child writes both streams. Retained buffers are
  bounded to 4096 bytes per stream; cancellation kills/reaps and joins readers.
  There are no grandchildren holding pipes; arbitrary descendant supervision is
  excluded. The outer test runner enforces a deadline.
- Plugin: plugin_host.rs and plugin_fixture.rs are exact snapshots of the existing
  local host/fixture. The oracle runs them inside a disposable working directory
  and compares state and transport cleanup. This does not prove malicious plugins
  cannot mutate other directories. A separate read probe exercises actual bwrap
  filesystem/PID/network isolation, with positive and negative read controls;
  it does not adopt a production Ox sandbox or test every kernel escape.
- Publication: a controlled local receiver checks its grant independently from
  the submitted APPROVED flag. Fixed fixture credentials are test data, not a
  deployable authentication protocol. Both rejected and permitted writes run.
- Iced: three-second worker, 40ms heartbeat, explicit focus routing from hidden
  detail input to command input and back, retained text, four fixed-width actions,
  and actual layout-call counts. Only documented sizes, local workload, X11 and
  observed font/rendering environment are accepted. These are separate from the
  product UI and its native Wayland obligations.

Reports and criterion reviews: `docs/validation/skill-consumers-20261101/`.
Historical errors, including clipped Quit at the minimum size, are preserved.
Current evidence is a content-bound observation, not general skill effectiveness,
future compatibility, code authenticity or authorization for product adoption.
