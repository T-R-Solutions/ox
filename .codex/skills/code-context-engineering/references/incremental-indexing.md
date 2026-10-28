# Generation-based index updates

Key a document by workspace identity and canonical project path, with a content hash distinct from its identity. A generation records parser configuration and input hashes. Stage changed entries and tombstones before publishing the generation; readers should not accidentally combine old definitions with new references.

[Tree-sitter advanced parsing](https://tree-sitter.github.io/tree-sitter/using-parsers/3-advanced-parsing.html) describes applying edits to the old tree before incremental parsing and updating retained node positions. This is syntax maintenance, not semantic call resolution. If using another parser, verify its invalidation contract rather than importing these API assumptions.

A rename can preserve conceptual symbol identity while changing file identity; require evidence for that mapping. If uncertain, remove/add with a documented alias rather than retaining stale offsets. Test delete, rename, ignored-file transition, parser failure and lost watcher event. Failed parsing should leave an explicit unavailable/stale generation, not a silently current old index.
