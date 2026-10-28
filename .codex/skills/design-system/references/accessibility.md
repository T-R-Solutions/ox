# Accessibility verification for interface changes

Use the target platform and agreed accessibility requirements. This guide supplies an investigation sequence, not a conformance certificate. Record the criterion, tested page/process, environment, evidence and unresolved exceptions.

## Select the applicable criteria

For web interfaces, consult the current [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) for applicable success criteria and exact exceptions. Check semantics and alternatives; keyboard access and focus; contrast and responsive presentation; error recovery, authentication and status changes. Preserve criterion levels rather than presenting every enhanced requirement as AA. Conformance concerns whole pages and complete processes; partial component checks cannot establish it.

## Verify actual interaction

**Action:** Prefer native controls matching intent; implement and test any custom behavior. **Context:** interactive components. **Evidence:** [APG read me first](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/), [button](https://www.w3.org/WAI/ARIA/apg/patterns/button/), [link](https://www.w3.org/WAI/ARIA/apg/patterns/link/). **Rationale:** exposed semantics create user expectations. **Exception/cost:** custom widgets can be justified, but add behavior and compatibility obligations. **Validation:** inspect the accessibility tree, visible name and keyboard activation in supported environments. A navigation link and a command button may share styling without sharing semantics.

**Action:** Keep focus visible and predictable; distinguish focus from selection. **Context:** dynamic content and composite controls. **Evidence:** [APG keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/). **Rationale:** users need to retain their place across operations. **Exception/cost:** disabled controls may remain discoverable within particular patterns; automatic selection can be disruptive when loading is slow. **Validation:** traverse with keyboard, remove the active item, switch input modes, and verify the resulting focus location. Test shortcut conflicts rather than assuming platform equivalence. The source contains unfinished shortcut passages; consult the concrete widget pattern and target platform.

**Action:** Implement a modal as a complete interaction contract. **Context:** an actual modal interruption is justified by the task. **Evidence:** [APG modal dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/). **Rationale:** modal semantics must agree with focus handling and outside-content behavior. **Exception/cost:** initial and restored focus depend on content and workflow; complex content should not automatically become one description string. **Validation:** check entry focus, traversal, escape/close behavior, background interaction and return to the trigger or logical next task location. Static pictures cannot establish these properties.

## Test beyond appearance

Use automated checks where useful, then manually exercise representative tasks, zoom/reflow, keyboard access, errors and relevant assistive technology. Record browser, operating system, input method, assistive technology and tested versions. Unsupported tests remain pending. Avoid destructive actions in production while evaluating recovery.

Book evidence: Kholmatova, chapter 9 PDF 213–243 and chapter 10 PDF 244–285; MacDonald, chapters 2–3 PDF 40–158 and chapter 5 PDF 209–237. Their historical examples motivate state/context inspection; current official guidance resolves concrete accessibility behavior. Neither framework adoption nor visual similarity proves accessibility.
