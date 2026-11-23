# Locally generated governance archives — 2026-11-18

Scope: the authorized R3-2 distribution regression repair. This changes the local
governance package build and its shared distribution boundary. It does not publish
an archive, alter the central Toolbox, accept a product feature, or delete history.

## Problem and alternatives

The observed local archive contains 3,750,490,162 expanded bytes in 17,322 members
and is 990,649,100 bytes compressed. The generic inspector's 128 MiB budget rejects
the outer container before extraction. Its payloads include retained historical
evidence required by preservation consumers. Removing that history or exempting
it from inspection would weaken the requested guarantees. Raising the generic
constant would also enlarge the budget for arbitrary nested archives.

The IDE shell feature, its evidence and its dedicated design page additionally
refer to application sources deliberately excluded from governance distribution.
Their inclusion leaves isolated copies with unresolved product references.

## Decision

1. Keep `inspect_bytes`, its 128 MiB recursive payload budget and depth limit
   unchanged for arbitrary payloads and nested archives. The locally generated
   outer ZIP instead has a finite inventory captured from trusted checkout inputs
   before build: canonical relative name, SHA-256, exact size and normalized mode.
   This changes the unit of the outer-container budget. It does **not** preserve
   the previous 128 MiB aggregate limit or authorize unlimited untrusted archives.
2. Generate a canonical forward-only ZIP with fixed timestamp, member order,
   regular-file attributes, compression method and write chunks. Modes normalize
   to 0755 for executable sources and 0644 otherwise; reject privileged mode bits,
   links, unsafe/reserved names and nonregular sources. Preserve receipt, scope
   and manifest content contracts. Record the Python/zlib build environment.
3. Inspect the resulting container by reserializing those external inputs into a
   byte comparator. Compare every byte and require exact EOF; do not take names,
   content identities or budget from the archive's own manifest. Bound source
   reads by observed size, verify their hashes/modes and apply the existing
   recursive inspector to every payload and generated metadata entry. Recheck the
   inventory around inspection and after the commands. Bind the ZIP identity
   before/after inspection and after extraction/verification.
4. Independently parse the inspected ZIP using `zipfile` into a new empty private
   directory. Require unique, exactly expected names and regular modes; check
   sizes and content hashes against the external inventory. Write only expected
   names, restore and verify modes, then compare the resulting manifest and scope.
   Execute all five established package commands and retain their output/exits.
5. Exclude exactly `sdd/features/product-ide-shell/`,
   `docs/validation/ide-shell-20261118/`, and the single page
   `docs/design/ide-shell.md` through the existing `product_record` seam. That seam
   affects ZIP, export-clean and other governance copies. Similar names remain
   included. Keep all three paths in the checkout and retain the feature in the
   applicable checkout acceptance selection. `task_finalizada.md` remains required.

## Trust and verification

The external inventory is a local build observation, not a signature or permission.
The trusted checkout, its review/VCS process and the observed Python/zlib runtime
are preconditions. Reproduction is qualified for that environment, not all ZIP
producers or future compression implementations. The comparator shares the
serializer with the builder, so exact identity alone cannot prove the serializer
correct: independent adversarial tests, parser/extraction checks and actual copied
commands are necessary. No general hostile-writer concurrency or OS sandbox
guarantee is added.

Rejections must cover prefix/suffix/metadata corruption, missing/duplicate/extra
members, hidden bytes after a DEFLATE end marker even when `zipfile` accepts the
plaintext, source inventory/content/mode drift, unsafe paths and links. Demonstrate
an aggregate above 128 MiB with bounded members, and rejection of excessive
individual and nested expansion/depth. Verify executable/nonexecutable modes,
both named R3-2 regressions, intact log links and the full independent package.
Expected negative failures are successful only when their explicit oracles agree.

The shared helper's byte succession is recorded through the existing schema-2
data registry with its authentic prior snapshot, this decision and independent
review. Do not update a Python hash constant or rewrite historical observations.
The task remains incomplete until integration, required executions, independent
review/validation and current evidence satisfy the user's full acceptance criteria.

Consumers reviewed: `distribution_files`, `copy_distribution`, `export-clean.py`,
`package-ox.py`, `check-ox.py`, isolated governance fixtures and the predecessor
chain through `document_ledger.py`. Recovery restores only this change from its
retained preimages, preserving unrelated source work, generated failure records
and all historical evidence.
