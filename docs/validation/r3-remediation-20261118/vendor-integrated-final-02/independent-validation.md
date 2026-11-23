# Independent validation of integrated layout run 02

The independent validator compared 167 observed inputs and nine binaries against
both before/after records and live bytes. All six externs match exact Cargo
PackageIDs and compiler artifacts; all streams match their recorded hashes.
Four real library tests passed with zero ignored/filtered. Invalid padding
produced E0080 and bool: Pod produced E0277, the required negative oracles.
The explicit locked/offline iced/wgpu-bare build passed. Licenses and patch
notices for both vendors were present and bound.

This supports layout and optional-build portions of dependency AC05 only. Final
scanners, whole-workspace evidence and criterion composition remain necessary.
No GPU runtime, upstream benchmarks/examples or transitive adapter SAST is
claimed. Hashbrown remains a separate mandatory Clippy blocker.
