#!/usr/bin/env bash
# shellcheck disable=SC2034 # Registry arrays/properties are consumed by entries.
# The only check/scope registry and argv definitions.
SECURITY=(gitleaks osv opengrep audit bandit)
QUALITY=(machete ruff deny)
OPTIONAL=(history coverage geiger trivy sbom grype malware shellcheck)
GOVERNANCE=(sdd-structure ox governance-tests)
RUST=(rust-fmt rust-check rust-build rust-test rust-clippy)
scope_checks() {
    case $1 in
        governance) BASE=("${GOVERNANCE[@]}");;
        rust) BASE=("${RUST[@]}");;
        security) BASE=("${SECURITY[@]}");;
        quality) BASE=("${QUALITY[@]}");;
        full) BASE=("${GOVERNANCE[@]}" "${RUST[@]}" "${SECURITY[@]}" "${QUALITY[@]}");;
        *) die "Unknown scope: $1";;
    esac
}
check_properties() {
    TOOL='' DATA='' RULE='' CONFIG='' SNAPSHOT=all
    case $1 in
        gitleaks|history) TOOL=gitleaks; RULE=gitleaks.toml;;
        osv) TOOL=osv-scanner; SNAPSHOT=none;;
        opengrep) TOOL=opengrep; RULE=ox.yml; SNAPSHOT=code;;
        audit) TOOL=cargo-audit; DATA=rustsec; SNAPSHOT=none;;
        deny) TOOL=cargo-deny; SNAPSHOT=none;;
        machete) TOOL=cargo-machete;;
        coverage) TOOL=cargo-llvm-cov;;
        geiger) TOOL=cargo-geiger;;
        trivy) TOOL=trivy;;
        sbom) TOOL=syft;;
        grype) TOOL=grype;;
        malware) TOOL=yr; RULE=suspicious.yar;;
        ruff) TOOL=ruff; SNAPSHOT=code;;
        bandit) TOOL=bandit; SNAPSHOT=code;;
        shellcheck) TOOL=shellcheck;;
        *) return 1;;
    esac
    case $1 in
        ruff) CONFIG=ruff.toml;; bandit) CONFIG=bandit.yaml;;
        audit) CONFIG=audit.toml;; deny) CONFIG=deny.toml;; osv) CONFIG=osv-scanner.toml;;
        shellcheck) CONFIG=shellcheckrc;; trivy) CONFIG=trivy.yaml;;
        sbom) CONFIG=syft.yaml;; grype) CONFIG=grype.yaml;;
    esac
    [[ $1 != history ]] || SNAPSHOT=none
}
check_command() {
    local name=$1 output=$2 source=${3:-\{source\}} db=${4:-\{reviewed-dataset\}}
    CWD=$ROOT
    case $name in
        sdd-structure) CMD=(python3 sdd/tools/validate.py --root . --structure-only);;
        ox) CMD=(python3 tools/governance/scripts/check-ox.py);;
        governance-tests) CMD=(python3 tools/governance/scripts/run-tests.py --group "${GROUP:-fast}");;
        rust-fmt) CMD=("${CARGO:-cargo}" fmt --all -- --check); CWD=$ROOT/application;;
        rust-check|rust-build|rust-test) CMD=("${CARGO:-cargo}" "${name#rust-}" --workspace --locked --offline); CWD=$ROOT/application;;
        rust-clippy) CMD=("${CARGO:-cargo}" clippy --workspace --all-targets --locked --offline -- -D warnings); CWD=$ROOT/application;;
        audit) CMD=(cargo-audit audit --no-fetch --no-yanked --db "$db" --file Cargo.lock --json --deny warnings); CWD=$output/audit-input;;
        deny) CMD=(cargo-deny deny --format json --config "$ROOT/scripts/config/deny.toml" --workspace --locked --offline check licenses bans sources); CWD=$ROOT/application;;
        machete) CMD=(cargo-machete machete --skip-target-dir --no-ignore .); CWD=$source/application;;
        coverage) CMD=(cargo-llvm-cov llvm-cov --workspace --locked --offline --no-clean --lcov --output-path "$output/coverage.lcov"); CWD=$source/application;;
        geiger) CMD=(cargo-geiger geiger --locked --offline --all-dependencies --output-format Json); CWD=$source/application;;
        *) die "Unknown check: $name";;
    esac
}

# All paths below are explicit container paths; no host-path rewriting.
native_command() {
    local rel
    : "$1"
    SCANNER=$TOOL
    case $name in history) SCANNER=gitleaks;; malware) SCANNER=yara-x;; esac
    local config=/project/scripts/config rules=/project/scripts/security/rules
    local -a targets=()
    case $name in
        ruff|bandit|shellcheck)
            while IFS= read -r -d '' rel; do
                case $name:$rel in
                    shellcheck:scripts/*.sh|ruff:*.py|bandit:*.py) targets+=("/project/$rel");;
                esac
            done < <(jq -j 'keys[] | ., "\u0000"' "${output:-}/inputs.json" 2>/dev/null)
            if ((${#targets[@]}==0)); then
                if [[ ${plan:-false} == true ]]; then targets=('{selected-files}'); else fail_check 'Empty scanner target selection'; fi
            fi ;;
    esac
    case $name in
        gitleaks|history)
            NATIVE=(dir --config "$rules/gitleaks.toml" --redact=100 --ignore-gitleaks-allow --exit-code 10 --report-format json --report-path /out/report.json)
            if [[ $name == history ]]; then NATIVE[0]=git; NATIVE+=(--log-opts=--all); fi
            NATIVE+=(/project);;
        osv) NATIVE=(scan source --offline --config "$config/osv-scanner.toml" --format json --all-packages --lockfile /project/application/Cargo.lock);;
        opengrep) NATIVE=(scan --config "$rules/ox.yml" --disable-version-check --strict --no-git-ignore --experimental --x-ignore-semgrepignore-files --disable-nosem --error --json /project);;
        trivy) NATIVE=(--config "$config/trivy.yaml" fs --scanners vuln --ignorefile "$config/trivyignore" --offline-scan --skip-db-update --skip-java-db-update --format json --exit-code 1 --cache-dir /cache /project);;
        grype) NATIVE=(--config "$config/grype.yaml" dir:/project -o json);;
        sbom) NATIVE=(--config "$config/syft.yaml" scan dir:/project -o syft-json);;
        malware) NATIVE=(scan --output-format json --recursive "$rules/suspicious.yar" /project);;
        ruff) NATIVE=(check --config "$config/ruff.toml" --ignore-noqa --no-fix --no-cache --output-format json "${targets[@]}");;
        bandit) NATIVE=(--configfile "$config/bandit.yaml" --ini "$config/bandit.ini" --ignore-nosec --baseline "$config/bandit-baseline.json" -f json "${targets[@]}");;
        shellcheck) NATIVE=(--rcfile "$config/shellcheckrc" --format=json "${targets[@]}");;
    esac
}
