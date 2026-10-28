---
name: software-delivery
description: Build, verify, package, promote, and release software through controlled inputs, dependency trust, pipelines, and recovery-aware rollouts. Use for build or release changes and diagnosis; skip ordinary code edits, team-productivity studies, and runtime incidents without a delivery question.
---

# Software Delivery

Own the path from source and build inputs to identified artifacts and a controlled
release. Discover project commands, toolchains, dependency graph, repositories,
lockfiles, CI configuration, permissions, environments, release consumers and recovery
requirements. Do not invent a pipeline, deployment policy or supported versions.

## Procedure

1. Define the artifact and contract being delivered, source revision, platform/variants,
   consumers and acceptance checks. Include generated code, configuration and migrations.
2. For build/dependency work read [build inputs and trust](references/build-inputs-and-trust.md).
   Diagnose resolution, caches and variable inputs before deleting caches or forcing
   versions. Pinning, hermeticity and reproduction are separate claims.
3. Implement the smallest reproducible setup and pipeline change supported by the
   project. Isolate untrusted contributions from privileged jobs, scope secrets and
   token permissions and verify caches cannot import untrusted outputs as trusted.
   Pipeline-as-code needs review and tested failure behavior, not just valid YAML.
4. For promotion/release work read [release and state](references/release-and-state.md).
   Promote the same immutable artifact by digest; bind configuration, schema prerequisites,
   version contracts, decision signals and state recovery to that release.
5. Execute proportionate checks in controlled environments: clean build, dependency
   divergence, failed stage, artifact identity and interrupted rollout/recovery where
   available. Record exact commands, inputs, environment, digests and observed result.

## Result and boundaries

Deliver working build/pipeline/release changes with decisions, checks and unverified
stages. No CI/CD, signature, SemVer label, SBOM or successful build alone proves
quality, compatibility, security or reproducibility. Never infer permission to publish
or deploy from this skill; follow the user's actual scope.

Language tools concretize this workflow; no Gradle, cloud, containers or orchestrator
is required. Reliability owns broader recovery goals, security owns threat/control
assessment and evolution owns long-lived coexistence. Use available specialists only
for unresolved needs; this folder works independently without any skill or SDD.
