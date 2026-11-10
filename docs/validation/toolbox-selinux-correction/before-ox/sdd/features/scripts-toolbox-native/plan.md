# Design and authority

Full workflow: contract/security/operational migration authorized by the user's
2026-11-08 request, limited to Ox, no commit or central maintenance.

D-01: Replace the existing backend in place with native exec. Keep registry,
files, process and report modules; reject a second executor or private imports.
D-02: Reject obsolete environment controls rather than ambiguous dual discovery.
D-03: Fail closed where central DB timestamps cannot enforce 24h/120h; Grype
uses its native 120h policy. Never pin consumer snapshots or change validity.
R-01: Mock transport cannot qualify actual scanner versions or Docker cleanup.
R-02: Central registry is empty; RustSec review expired; external maintenance
requires independently authorized operator work. No downloads in this task.

Selected primary skill: software-design, .codex/skills/software-design/SKILL.md;
no declared version; observed SHA256 4e214fd5dbf141ee437814a5c817b6924a05e8ad75cf6bc208281155204f6143. Contribution: responsibilities,
contract seam and proportionate removal of obsolete config/lock. No supporting
skill or sub-agent used. Compare leaving native-first dispatch (violates authority)
with adapting the existing modules (chosen); no new platform library.
