# Build inputs, reproduction and trust

Read for build diagnosis, dependencies or supply-chain claims.

Distinguish these claims before selecting a fix:

| Claim | Necessary evidence / limitation |
| --- | --- |
| Fixed versions | Resolved direct/transitive graph and immutable artifacts; coordinates alone may change |
| Hermetic build | Declared/controlled toolchains and inputs, excluding ambient dependencies; time/randomness may still vary |
| Reproducible specified artifacts | Independent rebuilds with stated source/environment/instructions and byte comparison |
| Provenance | Verified binding between artifact, builder, process and inputs; it can describe a nonreproducible build |
| SBOM | Inventory and identity of components; completeness and correspondence need checks |
| Signature | Trusted signer/policy and artifact integrity; does not prove correct source, safe code or independent reproduction |

Inventory compiler/linker/runtime, wrapper, plugins/processors, generated sources,
flags, OS/architecture, system libraries, direct/transitive dependencies, repository
rules, environment, timestamps, paths, locale/timezone, file ordering and randomness.
Use the project's locking mechanism for resolved versions and verify checksums/signers
through trusted metadata. Review lock and trust updates separately from version intent;
do not automatically trust freshly downloaded hashes. Balance updates with security
and compatibility checks; frozen vulnerable inputs are still vulnerable.

In Gradle, locking fixes selected configurations' resolved versions, while dependency
verification covers configured checksums/signatures. Catalogs alone are not locks.
Review bootstrap metadata rather than certifying whatever the repository returned.
This example does not mandate Gradle; discover its version and affected configurations.
[Locking](https://docs.gradle.org/current/userguide/dependency_locking.html),
[verification, bootstrapping](https://docs.gradle.org/current/userguide/dependency_verification.html).

Define the artifacts included in a reproduction claim, including archive metadata.
Rebuild in separate clean directories/environments with caches disabled or provenance
controlled; fetching the same cached artifact twice is not independent rebuilding.
Compare bytes/digests and inspect content/metadata differences. Normalize legitimate
variable inputs at creation (e.g. stable ordering/timestamps/path mapping) instead of
silently excluding differing files. If signatures or envelopes vary, specify and
compare unsigned payload separately and report the narrower claim.
[Definition](https://reproducible-builds.org/docs/definition/),
[variance topics](https://reproducible-builds.org/docs/).

Cache keys must include result-affecting inputs; test changed input, cold/hit result
and relocation. Restrict cache writers and secret access. Record trust boundaries
for hosted/self-hosted builders and reusable steps. SLSA provenance describes builder,
parameters and resolved dependencies; verify subject digest, builder identity and
expected process against project policy. Do not claim a SLSA level from a generated
JSON file or treat SLSA as a reproducibility certification.
[SLSA v1.2 provenance](https://slsa.dev/spec/v1.2/build-provenance),
[build track](https://slsa.dev/spec/v1.2/build-track-basics).

Validation should reject a substituted dependency and expose an intentionally variable
input before reporting the controlled artifact pair equal. Local reproduction remains
bounded to the tested artifacts/environments; no universal security conclusion follows.
