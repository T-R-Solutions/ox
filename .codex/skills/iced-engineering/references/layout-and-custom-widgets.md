# Layout, panes and custom widgets

Start with standard composition and stable content IDs. Persist logical pane placement and user preferences, then validate restored geometry against the current screen. Preserve content when a panel collapses; define whether focus moves to its toggle or another visible control. Reopening should restore a valid target rather than an invisible focused node.

Check the exact pane-grid and advanced Widget APIs in the installed Iced version before implementing callbacks or trait methods. The dedicated 0.14.0 pane-grid/Widget documentation URLs were unavailable during this authorship; no signatures from them are asserted here. Resolve this gap from versioned source/docs when applying the skill.

For a custom node view, specify hit testing, keyboard traversal, selected/hover/focus states, event capture versus propagation, clipping, scaling and accessible semantics. Test narrow/short windows and large text. A visually correct canvas does not establish keyboard or assistive-technology support.
