#!/usr/bin/env bash
# shellcheck disable=SC2034,SC2154 # Sourced module: runner supplies inputs and consumes result variables.
# Central catalog transport. Cargo utilities remain explicit local product tools.
select_backend() {
    BACKEND_REASON='' TOOL_BIN=''
    if [[ -n ${OX_TOOLBOX_BIN+x} || -n ${OX_SCANNER_BACKEND+x} ]]; then
        BACKEND_REASON='Obsolete OX_TOOLBOX_BIN/OX_SCANNER_BACKEND; remove them and use TOOLBOX_BIN or PATH'
        return 1
    fi
    # shellcheck disable=SC2153 # Assigned by check_properties in registry.sh.
    case ${EXECUTOR} in
        native)
            BACKEND=native
            [[ -z ${OX_CARGO_BIN+x} || -n ${OX_CARGO_BIN} ]] || {
                BACKEND_REASON='OX_CARGO_BIN is empty; select the installed Cargo plugins'
                return 1
            }
            if [[ -n ${NATIVE_EXECUTABLE_PATH:-} ]]; then
                local selected selected_sha
                selected=$(contained "${NATIVE_EXECUTABLE_PATH}") &&
                    [[ -f ${selected} && -x ${selected} ]] || {
                    BACKEND_REASON="Configured native executable missing, unsafe or not executable: ${NATIVE_EXECUTABLE_PATH}"
                    return 1
                }
                selected_sha=$(hash_file "${selected}") || return 1
                [[ ${selected_sha} == "${NATIVE_EXECUTABLE_SHA256}" ]] || {
                    BACKEND_REASON="Configured native executable digest mismatch: ${NATIVE_EXECUTABLE_PATH}"
                    return 1
                }
                TOOL_BIN=${selected}
                return 0
            fi
            # Like Ec, keep caller-selected tools before the Cargo plugin directory.
            export PATH="${PATH}:${OX_CARGO_BIN-${CARGO_HOME:-${HOME}/.cargo}/bin}"
            TOOL_BIN=$(command -v "${TOOL}" || true)
            [[ -n ${TOOL_BIN} ]] || { BACKEND_REASON="Required local Cargo utility unavailable: ${TOOL} (outside central catalog)"; return 1; };;
        *) BACKEND=toolbox; TOOL_BIN=${LIB_DIR}/../toolbox.sh;;
    esac
}
toolbox_command() {
    local executable=$1 source_path=$2 result_path=$3
    CMD=("${executable}" exec --tool "${SCANNER}" --project-root "${source_path}"
         --results "${result_path}" --timeout "${NATIVE_TIMEOUT}"
         --diagnostic-file "${result_path}/backend_record.json" -- "${NATIVE[@]}")
}
backend_plan() {
    CMD=() CWD=${ROOT}
    if [[ ${plan:-false} == true && ${legacy:-true} == false ]]; then
        BACKEND=${EXECUTOR}
        TOOL_BIN=${LIB_DIR}/../toolbox.sh
    else
        select_backend || { BACKEND=unavailable; return; }
    fi
    if [[ ${BACKEND} == toolbox ]]; then
        native_command "${name}" '{output}' true
        toolbox_command "${TOOL_BIN}" '{source}' '{output}'
    else
        check_command "${name}" '{output}'
        if [[ -n ${NATIVE_EXECUTABLE_PATH:-} ]]; then
            CMD[0]=${ROOT}/${NATIVE_EXECUTABLE_PATH}
        fi
    fi
}
run_toolbox() {
    local name=$1 source=$2 output=$3 tool=$4 tool_sha=$5
    local report before history_policy history_sha expected_history_sha reviewed_sha final_source_sha wrapper_sha
    [[ -z ${CONFIG} || -f ${source}/${CONFIG} ]] || fail_check POLICY_INVALID 'Missing native configuration'
    [[ -z ${RULE} || -f ${source}/${RULE} ]] || fail_check POLICY_INVALID 'Missing native rules'
    if [[ ${name} == history ]]; then
        history_policy=$(policy_path gitleaks-history.ignore) || return 1
        history_sha=$(hash_file "${source}/${history_policy}") || fail_check POLICY_INVALID 'Missing/changed reviewed history fingerprints'
        expected_history_sha=$(jq -r .reviews.history_sha256 <<<"${AUTOMATION_JSON}") || return 1
        [[ ${history_sha} == "${expected_history_sha}" ]] || fail_check POLICY_INVALID 'Missing/changed reviewed history fingerprints'
    fi
    if [[ ${name} == bandit || ${name} == ruff ]]; then
        local rel expected review
        review=$(jq -ce '.reviews.static | select((.sources|length)>0 and (.policy_files|length)>0)' "${source}/scripts/config/automation.json") || fail_check POLICY_INVALID 'Missing static review registry'
        capture_nul stream_fields jq -j '(.sources + .policy_files)|to_entries[]|.key,"\u0000",.value,"\u0000"' <<<"${review}" || return 1
        while IFS= read -r -d '' rel && IFS= read -r -d '' expected; do
            [[ ${rel} != /* && ${rel} != .. && ${rel} != ../* && ${rel} != */../* && ${rel} != */.. && ${expected} =~ ^[a-f0-9]{64}$ ]] || fail_check INPUT_INVALID 'Invalid reviewed source path or hash'
            if [[ -f ${source}/${rel} ]]; then
                reviewed_sha=$(hash_file "${source}/${rel}") || return 1
                [[ ${reviewed_sha} == "${expected}" ]] || fail_check INPUT_INVALID 'Reviewed static source changed; review required'
            elif [[ ${rel} == scripts/config/* ]]; then
                fail_check POLICY_INVALID 'Missing reviewed static policy'
            fi
        done < <(printf '%s\0' "${stream_fields[@]}")
    fi
    native_command "${name}" "${output}" false
    before=$(tree_identity "${source}") || fail_check INPUT_INVALID 'Cannot identify complete snapshot'
    EXECUTED=true
    toolbox_command "${tool}" "${source}" "${output}"
    execute "${output}/tool" "${ROOT}" "${CMD[@]}"
    RUNNER_RAW=${PROCESS_CODE}
    if [[ ${name} == trivy && -f ${output}/report.json ]]; then
        redact_trivy "${output}/report.json" "${output}" || fail_check REPORT_INVALID 'Invalid Trivy report; raw content withheld, see redaction identity'
    fi
    strict_json "${output}/backend_record.json" || fail_check EXECUTOR_INVALID "Missing/invalid native execution diagnostic (runner exit ${RUNNER_RAW}); inspect tool/stderr.log and TOOLBOX_BIN/PATH"
    RAW=$(jq -er 'if .native_exit_code==null then "null" elif (.native_exit_code|type)=="number" and (.native_exit_code|floor)==.native_exit_code and .native_exit_code>=0 and .native_exit_code<=255 then .native_exit_code else error("invalid native exit") end' "${output}/backend_record.json") || { RAW=null; fail_check EXECUTOR_INVALID 'Invalid diagnostic native exit'; }
    jq -e --arg tool "${SCANNER}" --argjson code "${PROCESS_CODE}" '
        .tool==$tool and .outcome=="native" and .cleanup=="removed" and
        (.version|type=="string" and length>0) and (.image|test("^sha256:[0-9a-f]{64}$")) and
        (.native_exit_code|type=="number" and floor==. and .>=0 and .<=255) and .native_exit_code==$code
    ' "${output}/backend_record.json" >/dev/null || fail_check EXECUTOR_INVALID 'Executor infrastructure, timeout, cancellation, cleanup or identity failure; inspect diagnostic'
    case ${name} in
        osv|trivy)
            validate_database_metadata "${output}/backend_record.json" "${name}" || fail_check DATASET_INVALID 'Invalid, inconsistent or expired central database metadata';;
        grype)
            jq -e '.database|type=="string" and test("^[0-9a-f]{64}$")' "${output}/backend_record.json" >/dev/null || fail_check DATASET_INVALID 'Missing central database identity';;
        *) :;; # Other validated classifications require no action.
    esac
    report=${output}/tool/stdout.log
    [[ ${name} != gitleaks && ${name} != history && ${name} != trivy ]] || report=${output}/report.json
    assess "${name}" "${RAW}" "${report}" || fail_check REPORT_INVALID 'Invalid/incomplete native report'
    # For native scanners, a clean report must have exit zero; findings must agree
    # with the chosen native exit policy (Grype/YARA return zero with findings).
    local expected=1
    case ${name} in gitleaks|history) expected=10;; grype|malware) expected=0;; *) :;; esac
    [[ ${COUNT} =~ ^[0-9]+$ && ${RAW} =~ ^[0-9]+$ ]] || fail_check REPORT_INVALID 'Invalid native report counts'
    [[ ( ${COUNT} == 0 && ${RAW} == 0 ) || ( ${COUNT} -gt 0 && ${RAW} == "${expected}" ) ]] || fail_check REPORT_INVALID 'Native findings and exit disagree'
    if ((COUNT>0)); then STATE=findings CODE=1; fi
    if [[ ${name} == opengrep ]]; then
        jq -e --slurpfile inputs "${output}/inputs.json" '.paths.scanned as $scanned |
          all($inputs[0]|keys[]|select(test("\\.(rs|py)$")); . as $p | ($scanned|index("/project/"+$p))!=null)' "${report}" >/dev/null || fail_check INPUT_INVALID 'SAST omitted selected input'
    fi
    if [[ ${name} == bandit ]]; then
        jq -e --slurpfile inputs "${output}/inputs.json" '.metrics as $metrics |
          all($inputs[0]|keys[]|select(endswith(".py")); . as $p | $metrics|has("/project/"+$p))' "${report}" >/dev/null || fail_check INPUT_INVALID 'Bandit omitted selected input'
    fi
    final_source_sha=$(tree_identity "${source}") || return 1
    if [[ ${final_source_sha} != "${before}" ]] || ! verify_inputs "${output}"; then
        fail_check INPUT_INVALID 'Input/snapshot changed'
    fi
    mkdir -- "${output}/recheck"
    source_snapshot "${output}/recheck" all || fail_check INPUT_INVALID 'Cannot verify final source selection'
    if ! cmp -s -- "${output}/inputs.json" "${output}/recheck/inputs.json" ||
        ! cmp -s -- "${output}/input_modes.json" "${output}/recheck/input_modes.json"; then
        fail_check INPUT_INVALID 'Source inventory or modes changed during scan'
    fi
    wrapper_sha=$(hash_file "${tool}") || return 1
    [[ ${wrapper_sha} == "${tool_sha}" ]] || fail_check TOOL_CHANGED 'Wrapper changed during check'
}

# OSV acquisition freshness belongs to Toolbox; upstream dates are provenance only.
# Trivy retains the consumer age policy on its native database timestamps.
validate_database_metadata() {
    local record=$1 age_policy=$2 limit oldest=9223372036854775807 value epoch effective current
    case ${age_policy} in
        osv) :;;
        trivy)
            catalog_load
            limit=$(jq -er '.databases.trivy.maximum_age_seconds | select(type=="number" and floor==. and .>0)' <<<"${AUTOMATION_JSON}") || return 1;;
        *) return 1;;
    esac
    jq -e '
      (.database|type=="string" and test("^[0-9a-f]{64}$")) and
      (.database_metadata as $m | $m.schema==1 and $m.snapshot==.database and
       $m.timestamp_semantics=="oldest_required_source" and
       ($m.data_timestamp|type=="string") and
       ($m.sources|type=="array" and length==2) and
       all($m.sources[]; (.url|type=="string" and startswith("https://")) and
         (.sha256|type=="string" and test("^[0-9a-f]{64}$")) and
         (.data_timestamp|type=="string") and
         (.timestamp_semantics=="upstream_object_generation_created" or
          .timestamp_semantics=="native_database_updated_at")))' "${record}" >/dev/null || return 1
    current=$(date -u +%s) || return 1
    local -a timestamps
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines timestamps jq -r '.database_metadata.sources[].data_timestamp' "${record}" || return 1
    for value in "${timestamps[@]}"; do
        [[ ${value} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$ ]] || return 1
        epoch=$(date -ud "${value}" +%s) || return 1
        if [[ ${age_policy} == trivy ]]; then
            ((epoch<=current && current-epoch<=limit)) || return 1
        fi
        ((epoch>=oldest)) || oldest=${epoch}
    done
    value=$(jq -r '.database_metadata.data_timestamp' "${record}") || return 1
    effective=$(date -ud "${value}" +%s) || return 1
    ((effective==oldest))
}
