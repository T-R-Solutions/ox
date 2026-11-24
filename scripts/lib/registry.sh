#!/usr/bin/env bash
# shellcheck disable=SC2154 # ROOT and SCRIPTS_DIR are initialized by common.sh before loading this module.
# shellcheck disable=SC2034 # Catalog properties are consumed by entries.
# Data ownership lives in config/automation.json; argv adapters remain explicit.
AUTOMATION_JSON=''
catalog_load() {
    [[ -z ${AUTOMATION_JSON:-} ]] || return 0
    local file=${SCRIPTS_DIR}/config/automation.json
    strict_json "${file}" || die 'Invalid automation JSON'
    AUTOMATION_JSON=$(cat -- "${file}")
    jq -e '
      .schema==1 and
      (.scopes|type=="object" and length>0) and
      (.checks|type=="object" and length>0) and
      (.optional|type=="array" and all(.[];type=="string")) and
      (.runtime.native_timeout|type=="number" and floor==. and .>0) and
      (.runtime.geiger_stack_bytes|type=="number" and floor==. and .>0) and
      (.runtime.clippy_flags|type=="array" and length>0 and all(.[];type=="string" and length>0)) and
      all(.policies[]; type=="string" and startswith("scripts/") and
          ((split("/")|index(".."))==null) and (explode|all(.[];.>=32))) and
      all(.checks[]; (.executor=="native" or .executor=="toolbox") and
          (if has("executable") then
             .executor=="native" and (.executable|type=="object" and keys==["path","sha256"]) and
             (.executable.path|type=="string" and length>0 and (startswith("/")|not) and
                (explode|all(.[];.>=32 and .!=127)) and
                (split("/")|all(.[];.!="" and .!="." and .!=".."))) and
             (.executable.sha256|type=="string" and test("^[a-f0-9]{64}$"))
           else true end) and
          (.snapshot=="none" or .snapshot=="code" or .snapshot=="all") and
          (.native_timeout==null or (.native_timeout|type=="number" and floor==. and .>0)) and
          (.tool|type=="string" and length>0)) and
      (. as $c | all(.checks[]; .policy==null or ($c.policies[.policy]|type=="string")))
    ' <<<"${AUTOMATION_JSON}" >/dev/null || die 'Invalid automation catalog schema'
    jq -e '
      . as $c |
      ([.scopes[][], "scripts-syntax", "scripts-tests"]|unique) as $known |
      .selection as $s |
      ($s.surfaces|type=="object" and length>0) and
      all($s.surfaces[];type=="array" and length>0 and length==(unique|length) and
          all(.[];. as $n|$known|index($n)!=null)) and
      ($s.mandatory|type=="array" and length>0 and all(.[];. as $n|$s.surfaces|has($n))) and
      ($s.aliases|type=="object" and all(.[];type=="array" and length>0)) and
      ($s.complete_only|type=="array") and ($s.explicit_surface|type=="array") and
      all($s.complete_only[], $s.explicit_surface[], $s.aliases[][];
          . as $n|[$s.surfaces[][]]|index($n)!=null) and
      (.environment.defaults|type=="object" and all(to_entries[];
          (.key|IN("LANG","LC_ALL","NO_COLOR","PYTHONDONTWRITEBYTECODE","RUSTUP_AUTO_INSTALL","CARGO_NET_OFFLINE","TOOLBOX_SELINUX_LABEL")) and
          (.value|type=="string" and (contains("\u0000")|not)))) and
      (.discovery.toolbox|type=="array" and all(.[];type=="string" and (explode|all(.[];.>=32))))
    ' <<<"${AUTOMATION_JSON}" >/dev/null || die 'Invalid selection/environment catalog'
    # Validate paths and source/review selectors before they reach find or files.
    jq -e '
      def text: type=="string" and length>0 and (explode|all(.[];.>=32 and .!=127));
      def relative: text and (startswith("/")|not) and
        (split("/")|all(.[];.!="" and .!="." and .!=".."));
      def digest: type=="string" and test("^[a-f0-9]{64}$");
      def bindings: type=="object" and length>0 and
        all(to_entries[]; (.key|relative) and (.value|digest));
      (.inputs|type=="object" and
        keys==["exclude_names","exclude_paths","root_patterns","roots"]) and
      (.inputs.roots|type=="array" and length>0 and all(.[];relative)) and
      (.inputs.root_patterns|type=="array" and length>0 and all(.[];text and (contains("/")|not))) and
      (.inputs.exclude_names|type=="array" and all(.[];text and (contains("/")|not))) and
      (.inputs.exclude_paths|type=="array" and all(.[];relative)) and
      (.paths|type=="object" and keys==["cargo","datasets","root","runs"] and all(.[];relative)) and
      (.databases|type=="object" and keys==["trivy"]) and
      (.databases.trivy|type=="object" and keys==["maximum_age_seconds"]) and
      (.databases.trivy.maximum_age_seconds|type=="number" and floor==. and .>0) and
      (.reviews|type=="object" and keys==["history_sha256","static"]) and
      (.reviews.history_sha256|digest) and
      (.reviews.static|type=="object" and keys==["policy_files","reason","sources"]) and
      (.reviews.static.reason|text) and
      (.reviews.static.sources|bindings) and (.reviews.static.policy_files|bindings)
    ' <<<"${AUTOMATION_JSON}" >/dev/null || die 'Invalid inputs/paths/databases/reviews catalog'
    local scope check
    local -a scopes=() checks=()
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines scopes jq -r '.scopes|keys[]' <<<"${AUTOMATION_JSON}" || return 1
    for scope in "${scopes[@]}"; do
        jq -e --arg scope "${scope}" '.scopes[$scope]|type=="array" and length>0 and length==(unique|length) and all(.[];type=="string")' <<<"${AUTOMATION_JSON}" >/dev/null || die 'Invalid scope'
        # shellcheck disable=SC2016 # jq variables belong to the quoted program.
        capture_lines checks jq -r --arg scope "${scope}" '.scopes[$scope][]' <<<"${AUTOMATION_JSON}" || return 1
        for check in "${checks[@]}"; do
            case ${check} in sdd-structure|ox|governance-tests|scripts-syntax|scripts-tests|rust-fmt|rust-check|rust-build|rust-test|rust-clippy) continue;; *) :;; esac
            jq -e --arg check "${check}" '.checks|has($check)' <<<"${AUTOMATION_JSON}" >/dev/null || die "Unknown catalog check: ${check}"
        done
    done
}
policy_path() {
    catalog_load
    jq -er --arg key "$1" '.policies[$key] // error("Unknown policy")' <<<"${AUTOMATION_JSON}"
}
scope_checks() {
    catalog_load
    jq -e --arg scope "$1" '.scopes|has($scope)' <<<"${AUTOMATION_JSON}" >/dev/null || die "Unknown scope: $1"
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines BASE jq -r --arg scope "$1" '.scopes[$scope][]' <<<"${AUTOMATION_JSON}" || return 1
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines OPTIONAL jq -r '.optional[]' <<<"${AUTOMATION_JSON}" || return 1
}
check_properties() {
    catalog_load
    local row policy
    row=$(jq -ce --arg name "$1" '.checks[$name] // empty' <<<"${AUTOMATION_JSON}") || return 1
    TOOL=$(jq -r .tool <<<"${row}")
    DATA=$(jq -r '.dataset // ""' <<<"${row}")
    SNAPSHOT=$(jq -r .snapshot <<<"${row}")
    EXECUTOR=$(jq -r .executor <<<"${row}")
    NATIVE_EXECUTABLE_PATH=$(jq -r '.executable.path // ""' <<<"${row}")
    NATIVE_EXECUTABLE_SHA256=$(jq -r '.executable.sha256 // ""' <<<"${row}")
    NATIVE_TIMEOUT=$(jq -r --arg name "$1" '.checks[$name].native_timeout // .runtime.native_timeout' <<<"${AUTOMATION_JSON}")
    CONFIG='' RULE=''
    policy=$(jq -r '.policy // empty' <<<"${row}")
    [[ -z ${policy} ]] || CONFIG=$(policy_path "${policy}")
}
check_command() {
    local name=$1 output=$2 source=${3:-\{source\}} db=${4:-\{reviewed-dataset\}}
    local clippy_policy clippy_dir
    CWD=${ROOT}
    case ${name} in
        sdd-structure) CMD=(python3 sdd/tools/validate.py --root . --structure-only);;
        ox) CMD=(python3 tools/governance/scripts/check-ox.py);;
        governance-tests) CMD=(python3 tools/governance/scripts/run-tests.py --group "${GROUP:-fast}");;
        scripts-syntax) CMD=(bash "${SCRIPTS_DIR}/check.sh");;
        scripts-tests) CMD=(python3 -m unittest discover -s scripts/tests -v);;
        rust-fmt) CMD=("${CARGO:-cargo}" fmt --all -- --check); CWD=${ROOT}/application;;
        rust-check|rust-build|rust-test) CMD=("${CARGO:-cargo}" "${name#rust-}" --workspace --locked --offline); CWD=${ROOT}/application;;
        rust-clippy)
            local -a flags
            catalog_load
            # shellcheck disable=SC2016 # jq variables belong to the quoted program.
            capture_lines flags jq -r '.runtime.clippy_flags[]' <<<"${AUTOMATION_JSON}" || return 1
            clippy_policy=$(policy_path clippy.toml) || return 1
            clippy_dir=$(dirname -- "${clippy_policy}") || return 1
            CMD=(env "CLIPPY_CONF_DIR=${ROOT}/${clippy_dir}" "${CARGO:-cargo}" clippy --workspace --all-targets --all-features --locked --offline --keep-going -- "${flags[@]}")
            CWD=${ROOT}/application;;
        audit) CMD=(cargo-audit audit --no-fetch --no-yanked --db "${db}" --file Cargo.lock --json --deny warnings); CWD=${output}/audit-input;;
        deny) CMD=(cargo-deny deny --format json --config "${ROOT}/$(policy_path deny.toml)" --workspace --all-features --locked --offline check licenses bans sources); CWD=${ROOT}/application;;
        machete) CMD=(cargo-machete machete --skip-target-dir --no-ignore .); CWD=${source}/application;;
        coverage) CMD=(cargo-llvm-cov llvm-cov --workspace --locked --offline --no-clean --lcov --output-path "${output}/coverage.lcov"); CWD=${source}/application;;
        geiger) CMD=(cargo-geiger geiger --locked --offline --all-dependencies --all-features --output-format Json); CWD=${source}/application;;
        *) die "Unknown check: ${name}";;
    esac
}

# Vendored third-party root excluded from Opengrep only (ADR verification-repair-20261123);
# the SAST coverage guard in backends.sh exempts exactly this root.
OPENGREP_EXCLUDED_ROOT=application/vendor
# All paths below are explicit container paths; no host-path rewriting.
native_command() {
    local name=$1 output=$2 plan=$3 rel policy_key policy_rel bandit_ini bandit_baseline
    local -a stream_fields=()
    SCANNER=${TOOL}
    case ${name} in history) SCANNER=gitleaks;; malware) SCANNER=yara-x;; *) :;; esac
    local policy
    policy_key=$(jq -r --arg name "${name}" '.checks[$name].policy' <<<"${AUTOMATION_JSON}") || return 1
    policy_rel=$(policy_path "${policy_key}") || return 1
    policy=/project/${policy_rel}
    local -a targets=()
    case ${name} in
        ruff|bandit|shellcheck)
            stream_fields=()
            if [[ ${plan:-false} != true ]]; then
                capture_nul stream_fields jq -j 'keys[] | ., "\u0000"' "${output:-}/inputs.json" || return 1
            fi
            for rel in "${stream_fields[@]}"; do
                case ${name}:${rel} in
                    shellcheck:scripts/*.sh|ruff:*.py|bandit:*.py) targets+=("/project/${rel}");;
                    *) :;; # Other validated classifications require no action.
                esac
            done
            if ((${#targets[@]}==0)); then
                if [[ ${plan:-false} == true ]]; then targets=('{selected-files}'); else fail_check REPORT_INVALID 'Empty scanner target selection'; fi
            fi ;;
        *) :;; # Other validated classifications require no action.
    esac
    case ${name} in
        gitleaks|history)
            NATIVE=(dir --config "${policy}" --redact=100 --ignore-gitleaks-allow --exit-code 10 --report-format json --report-path /out/report.json)
            if [[ ${name} == history ]]; then
                NATIVE[0]=git
                NATIVE+=(--log-opts=--all --gitleaks-ignore-path "/project/$(policy_path gitleaks-history.ignore)")
            fi
            NATIVE+=(/project);;
        osv) NATIVE=(scan source --offline --config "${policy}" --format json --all-packages --lockfile /project/application/Cargo.lock);;
        opengrep) NATIVE=(scan --config "${policy}" --config "/project/$(policy_path rust.yml)" --disable-version-check --strict --no-git-ignore --experimental --x-ignore-semgrepignore-files --disable-nosem --max-target-bytes 0 --taint-intrafile --timeout 0 --timeout-threshold 0 --error --json --exclude "/${OPENGREP_EXCLUDED_ROOT}" /project);;
        trivy) NATIVE=(--config "${policy}" fs --quiet --ignorefile "/project/$(policy_path trivyignore)" --offline-scan --skip-db-update --skip-java-db-update --skip-check-update --format json --output /out/report.json --list-all-pkgs --include-dev-deps --include-non-failures --exit-code 1 /project);;
        grype) NATIVE=(--config "${policy}" dir:/project -o json);;
        sbom) NATIVE=(--config "${policy}" scan dir:/project -o syft-json);;
        malware) NATIVE=(scan --output-format json --recursive "${policy}" /project);;
        ruff) NATIVE=(check --config "${policy}" --ignore-noqa --no-fix --no-cache --output-format json "${targets[@]}");;
        bandit)
            bandit_ini=$(policy_path bandit.ini) || return 1
            bandit_baseline=$(policy_path bandit-baseline.json) || return 1
            NATIVE=(--quiet --configfile "${policy}" --ini "/project/${bandit_ini}" --ignore-nosec --baseline "/project/${bandit_baseline}" -f json "${targets[@]}");;
        shellcheck) NATIVE=(--rcfile "${policy}" --format=json "${targets[@]}");;
        *) :;; # Other validated classifications require no action.
    esac
}
