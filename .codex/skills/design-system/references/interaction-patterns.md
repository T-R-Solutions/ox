# Shared patterns for operational interfaces

Consult only the pattern present in the requested interface. These contracts
supplement [visual composition](visual-composition.md); they are not a screen quota.

| Pattern and purpose | Define before styling | Exercise in the consumer |
| --- | --- | --- |
| Navigation and master/detail | Scope and active location; selection separate from hover/focus; back/return context; discoverable collapsed labels | Long navigation, missing selection, keyboard traversal, collapse/reopen and narrow layout |
| Command palette | Command/category/scope, active result, query and no-result recovery; shortcut conflicts; modal or nonmodal behavior; consequences of commands | Open by keyboard and pointer, traverse results, execute, Escape and restore focus; invalid/unavailable command; changing results while navigating |
| Workbench panes and tabs | Stable content identity, open versus selected versus modified; resize bounds, scroll ownership and panel recovery | Resize at min/max, close active tab, preserve unsaved work, reopen hidden pane and maintain a visible focus target |
| Board | State meaning and permitted moves; drag handle separate from controls; destination feedback; non-drag movement alternative | Move with keyboard/menu, empty destination, rejected move, long column, selection retained after relocation |
| Settings form | Setting scope, labels/help/errors, saved versus edited versus tested, effect of apply/reset; sensitive-value display | Invalid input retained, error summary when needed, pending/failed save, navigation with edits, test result distinct from persisted configuration |
| Operational table | Primary identity column, widths by content type, sort/filter scope, selection scope across pages and bulk consequences | No records versus no matches versus failed load; sorting after selection; long cells; narrow view with essential comparison/actions intact |
| Dashboard | User question, metric identity/unit/period/source, filter scope and drill-down; partial widget failure distinct from whole-page failure | Missing values versus zero, mixed freshness, retry one failed region, same quantity formatting across cards/charts/details |
| Terminal with GUI controls | Operation identity, working context, actual lifecycle, raw output versus summary, wrapping/scroll/follow behavior | Long lines, noisy output, user scrolled away, pending cancellation versus observed stop, failure details reachable |
| Conversation and tool inspector | Draft/stream/tool/result ownership; pending work and stop state; source/result provenance; composer key behavior | Long streaming output, failed/partial tool result, stop request, multiline/IME input, inspector collapse without losing the draft |
| Floating utility | Focus policy, user-controlled pinning, drag area separate from controls, close/reopen and position recovery | Small work area, large text, focus return, hidden/off-screen position and an unavailable always-on-top feature |

Model only effects supported by the actual consumer. A screenshot of a pin, save,
run or cancel button does not implement the OS, persistence or execution behavior.
Choose confirmation and recovery by the real consequence and existing policy;
do not add a universal dialog to every action. For keyboard and accessibility
behavior use the target platform's actual control contract and the applicable
[verification guidance](accessibility.md).

Source basis: original synthesis from the [desktop pack](https://github.com/umutc6230/ui-design-skills-pack/tree/4ffc9d638e32f1332fc7ac74e3060e6278743d4b/skills),
03–05 and 08–15, inspected 2026-11-16. Numeric presets, sample prompts, automatic
persistence and mandatory regions were deliberately excluded. Examples describe
design/verification obligations, not observed implementation.
