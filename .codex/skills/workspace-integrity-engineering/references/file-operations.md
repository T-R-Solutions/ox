# Safe write boundaries

A write intent contains root identity, relative path, base hash, proposed bytes/hash and operation kind. Validate both the input path and the object reached at the moment of use. String-prefix checks confuse sibling roots; simple canonicalization can race with symlink replacement. Choose platform capabilities appropriate to the trust model and test them on the target OS.

Use a same-filesystem temporary file when replacement semantics are required. [Rust rename](https://doc.rust-lang.org/std/fs/fn.rename.html) documents cross-filesystem failure and platform differences. Rename alone does not provide a portable multi-file transaction or proof of durability.

For crash recovery, journal intended/base/new identities and commit progress. On restart compare actual bytes with both base and staged hashes. If neither matches, preserve all candidates and report conflict. Do not infer completion merely because the temporary file disappeared. Tests should inject failure between staging, flushing, replacement and completion recording.
