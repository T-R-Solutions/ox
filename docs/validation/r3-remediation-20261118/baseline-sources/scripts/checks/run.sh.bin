#!/usr/bin/env bash
# Standalone scanner adapter, also called by automate.sh.
# shellcheck source=../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib/common.sh"
# shellcheck source=../lib/process.sh
source "${LIB_DIR}/process.sh"
# shellcheck source=../lib/registry.sh
source "${LIB_DIR}/registry.sh"
# shellcheck source=../lib/files.sh
source "${LIB_DIR}/files.sh"
# shellcheck source=../lib/reports.sh
source "${LIB_DIR}/reports.sh"
# shellcheck source=../lib/backends.sh
source "${LIB_DIR}/backends.sh"
main() {
name='' output='' inspect='' plan=false
manifests=()
while (($#)); do
    case $1 in
        --root|--check|--output|--inspect-data)
            (($#>=2)) || die "Missing value: $1"
            case $1 in --root) ROOT=$2;; --check) name=$2;; --output) output=$2;; --inspect-data) inspect=$2;; *) :;; esac
            shift 2;;
        --plan) plan=true; shift;;
        --help|-h) printf 'Usage: checks/run.sh [--root PATH] --check NAME [--plan] [--output DIR]\n       checks/run.sh --inspect-data RELATIVE_PATH\n'; exit 0;;
        *) die "Unknown argument: $1";;
    esac
done
ROOT=$(cd -- "${ROOT}" && pwd -P) || die 'Repository root missing'
if [[ -n ${inspect} ]]; then
    [[ -z ${name} && -z ${output} ]] || die 'inspect-data is exclusive'
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    data_path=$(contained "${inspect}") || die 'Dataset must stay relative to repository without symlinks'
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    identity=$(tree_identity "${data_path}") || die 'Invalid dataset tree'
    jq -n --arg path "${inspect}" --arg sha "${identity}" '{path:$path,sha256:$sha,freshness:"not reviewed"}'
    exit 0
fi
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
check_properties "${name}" || die "Unknown check: ${name}"
if ${plan}; then
    backend_plan
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    argv_json=$(json_args "${CMD[@]}") || exit 2
    jq -n --arg check "${name}" --arg backend "${BACKEND}" --arg tool "${TOOL}" --arg data "${DATA}" --argjson argv "${argv_json}" \
      '{check:$check,backend:$backend,tool:$tool,dataset:(if $data=="" then null else $data end),argv:$argv,per_workspace_member:($check=="geiger")}'
    exit 0
fi
owned_run=false
if [[ -z ${output} ]]; then
    output=$(new_run "security-${name}")
    run_lease "${output}"
    owned_run=true
else
    [[ -n ${OX_ACTIVE_RUN:-} && ${output} == "${OX_ACTIVE_RUN}/${name}" && -f ${OX_ACTIVE_RUN}/.owner ]] || die 'Output must belong to the active temporary run'
    [[ ! -L ${output} ]] || die 'Symlinked output'
    [[ -d ${output} ]] || die 'Explicit output directory must already exist'
fi
[[ ! -e ${output}/assessment.json && ! -e ${output}/tool ]] || die 'Output already used'
chmod 700 -- "${output}"
STATE=blocked CODE=3 RAW=null RUNNER_RAW=null EXECUTED=false COUNT=null REASON='' REASON_CODE='' PREPARED='' tool='' tool_sha='' BACKEND=native
# shellcheck disable=SC2329 # Invoked by the EXIT trap, including error exits.
finish() {
    local rc=$?
    trap - EXIT
    if ((rc)) && [[ -z ${REASON} ]]; then REASON='Check ended without a classified cause'; REASON_CODE=UNKNOWN; fi
    if [[ -n ${REASON} ]]; then
        if [[ ${RAW} == null && ${EXECUTED} == false ]]; then STATE=blocked CODE=3; else STATE=error CODE=2; fi
    fi
    jq -n --arg backend "${BACKEND}" --arg name "${name}" --arg state "${STATE}" --arg reason "${REASON}" --arg reason_code "${REASON_CODE}" --argjson code "${CODE}" --argjson runner "${RUNNER_RAW}" --argjson raw "${RAW}" --argjson count "${COUNT}" \
      --arg tool "${tool}" --arg sha "${tool_sha}" --arg output "${output}" \
      '{check:$name,backend:$backend,state:$state,exit_code:$code,tool_exit_code:$raw,runner_exit_code:$runner,finding_count:$count,reason:$reason,reason_code:$reason_code,product_acceptance:false,
        tool:{path:$tool,sha256:$sha},limits:["No automatic product acceptance.","Generated directories and historical validation excluded; history is separate.","Offline flags are not OS isolation."]}' >"${output}/assessment.tmp"
    local field
    for field in inputs dataset member_results backend_record backend_inputs; do
        if [[ -f ${output}/${field}.json ]]; then
            jq --arg field "${field}" --slurpfile value "${output}/${field}.json" '.+{($field):$value[0]}' "${output}/assessment.tmp" >"${output}/assessment.next"
            mv -- "${output}/assessment.next" "${output}/assessment.tmp"
        fi
    done
    if [[ -f ${output}/command.json ]]; then
        jq --slurpfile command "${output}/command.json" '.+$command[0]' "${output}/assessment.tmp" >"${output}/assessment.next"
        mv -- "${output}/assessment.next" "${output}/assessment.tmp"
    fi
    if [[ -f ${output}/version/stdout.log ]]; then
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        version_sha=$(hash_file "${output}/version/stdout.log") || exit 2
        jq --arg sha "${version_sha}" '.tool.version_stdout_sha256=$sha' "${output}/assessment.tmp" >"${output}/assessment.next"
        mv -- "${output}/assessment.next" "${output}/assessment.tmp"
    fi
    mv -n -- "${output}/assessment.tmp" "${output}/assessment.json"
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    if ${owned_run}; then run_complete "${output}" || exit 2; fi
    exit "${CODE}"
}
trap 'finish' EXIT
fail_check() { REASON_CODE=$1; shift; REASON=$*; exit 1; }
# Remove inherited scanner controls which could suppress results or enable updates.
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
capture_lines stream_fields compgen -e || exit 2
for key in "${stream_fields[@]}"; do
    case ${key} in GITLEAKS_*|SEMGREP_*|OPENGREP_*|GRYPE_*|SYFT_*|TRIVY_*|OSV_SCANNER_*|OSV_SCALIBR_*|RUFF_*|BANDIT_*) unset "${key}";; *) :;; esac
done
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
select_backend || fail_check POLICY_INVALID "${BACKEND_REASON:-required tool missing: ${TOOL}; invalid explicit backend configuration}"
tool=${TOOL_BIN}
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
current_tool_sha=$(hash_file "${tool}") || exit 2
if [[ -n ${NATIVE_EXECUTABLE_SHA256:-} && ${current_tool_sha} != "${NATIVE_EXECUTABLE_SHA256}" ]]; then
    fail_check TOOL_CHANGED 'Configured native executable changed after selection'
fi
tool=$(realpath -e -- "${tool}"); tool_sha=${current_tool_sha}
if [[ ${TOOL} == cargo-* ]]; then
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    installed_cargo || fail_check TOOL_UNAVAILABLE 'Required installed Rust toolchain unavailable'
fi
if [[ ${name} == coverage ]]; then
    llvm_cov=$(find "${CARGO%/bin/cargo}/lib/rustlib" -name llvm-cov -type f -print -quit) || exit 2
    llvm_profdata=$(find "${CARGO%/bin/cargo}/lib/rustlib" -name llvm-profdata -type f -print -quit) || exit 2
    [[ -n ${llvm_cov} && -n ${llvm_profdata} ]] || fail_check TOOL_UNAVAILABLE 'Installed llvm-tools-preview required'
fi
if [[ ${BACKEND} == toolbox ]]; then
    printf '{}\n' >"${output}/inputs.json"
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    source_snapshot "${output}" all || fail_check INPUT_INVALID 'Cannot create complete source snapshot'
    source=${output}/source
    if [[ ${name} == history ]]; then
        shallow=$(git -C "${ROOT}" rev-parse --is-shallow-repository) || exit 2
        [[ ${shallow} == false && -d ${ROOT}/.git && ! -L ${ROOT}/.git ]] || fail_check INPUT_INVALID 'Full self-contained Git history required'
        [[ ! -e ${ROOT}/.git/objects/info/alternates && ! -e ${ROOT}/.git/commondir ]] || fail_check INPUT_INVALID 'External Git object storage is unsupported'
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        git_before=$(tree_identity "${ROOT}/.git") || fail_check INPUT_INVALID 'Unsafe Git metadata'
        cp -a -- "${ROOT}/.git" "${source}/.git"
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        copied_git_sha=$(tree_identity "${source}/.git") || exit 2
        [[ ${copied_git_sha} == "${git_before}" ]] || fail_check INPUT_INVALID 'Git copy changed'
    fi
    [[ ${name} != opengrep ]] || : >"${source}/.semgrepignore"
    run_toolbox "${name}" "${source}" "${output}" "${tool}" "${tool_sha}"
    if [[ ${name} == history ]]; then
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        current_git_sha=$(tree_identity "${ROOT}/.git") || fail_check INPUT_INVALID 'Cannot identify Git history'
        [[ ${current_git_sha} == "${git_before}" ]] || fail_check INPUT_INVALID 'Git history changed'
    fi
    exit 0
fi
version=("${tool}" --version)
if [[ ${TOOL} == cargo-* ]]; then version=("${tool}" "${TOOL#cargo-}" --version); fi
execute "${output}/version" "${ROOT}" "${version[@]}"
((PROCESS_CODE==0)) || fail_check TOOL_UNAVAILABLE 'Cannot identify required tool version'
db='{reviewed-dataset}' source='{source}'
if [[ -n ${DATA} ]]; then
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    reviewed_dataset "${DATA}" "${output}" || fail_check DATASET_INVALID "Missing/invalid reviewed dataset: ${DATA}"
    db=${output}/dataset
fi
if [[ -n ${CONFIG} ]]; then
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    policy=$(contained "${CONFIG}") && [[ -f ${policy} ]] || fail_check POLICY_INVALID "Missing required scanner configuration: ${CONFIG}"
fi
printf '{}\n' >"${output}/inputs.json"
input_add "${output}" scripts/config/automation.json
if [[ ${SNAPSHOT} != none ]]; then
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    source_snapshot "${output}" "${SNAPSHOT}" || fail_check INPUT_INVALID 'Cannot create complete source snapshot'
    source=${output}/source
fi
for rel in application/Cargo.toml application/Cargo.lock application/rust-toolchain.toml; do
    [[ ! -e ${ROOT}/${rel} ]] || input_add "${output}" "${rel}"
done
[[ -z ${RULE} ]] || input_add "${output}" "${RULE}"
dataset_registry=$(local_path datasets)/datasets.json
[[ -z ${DATA} ]] || input_add "${output}" "${dataset_registry#"${ROOT}"/}"
[[ -z ${CONFIG} ]] || input_add "${output}" "${CONFIG}"
if [[ ${name} == coverage || ${name} == geiger ]]; then export CARGO_TARGET_DIR=${output}/target; fi
if [[ ${name} == coverage ]]; then export CARGO_LLVM_COV_TARGET_DIR=${output}/target CARGO_LLVM_COV_SETUP=no; fi
if [[ ${name} == audit ]]; then
    mkdir -p -- "${output}/audit-input/.cargo"
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    audit_policy=$(policy_path audit.toml) || exit 2
    cp -- "${ROOT}/${audit_policy}" "${output}/audit-input/.cargo/audit.toml"
    cp -- "${ROOT}/application/Cargo.lock" "${output}/audit-input/Cargo.lock"
fi
check_command "${name}" "${output}" "${source}" "${db}"
CMD[0]=${tool}
jq -n --arg cwd "${CWD}" '{cwd:$cwd,argv_recorded:false}' >"${output}/command.json"
if [[ ${name} == geiger ]]; then
    mkdir -- "${output}/tool"
    geiger_stack=$(jq -er '.runtime.geiger_stack_bytes' <<<"${AUTOMATION_JSON}") || fail_check POLICY_INVALID 'Invalid Geiger stack configuration'
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    metadata=$(workspace_metadata) || fail_check REPORT_INVALID 'Cannot enumerate workspace members'
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    capture_lines manifests jq -r '.workspace_members as $members | .packages[] | select(.id as $id|$members|index($id)) | .manifest_path' <<<"${metadata}" || exit 2
    ((${#manifests[@]})) || fail_check REPORT_INVALID 'Empty workspace'
    printf '[]\n' >"${output}/member_results.json"
    jq -n --argjson total "${#manifests[@]}" '{schema:1,completed:0,total:$total,activity:"membros"}' >"${output}/progress.json"
    final_code=0 final_raw=0 i=0 incomplete=false
    for manifest in "${manifests[@]}"; do
        # Cargo paths are parsed, not inferred from globbed directory names.
        # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
        validate_member_manifest "${manifest}" || fail_check REPORT_INVALID 'Workspace member escaped root'
        manifest=${source}/application/${manifest#"${ROOT}/application/"}
        execute "${output}/tool/${i}" "${CWD}" env "RUST_MIN_STACK=${geiger_stack}" "${CMD[@]}" --manifest-path "${manifest}"
        RAW=${PROCESS_CODE}
        member_reason=''
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        if ! assess "${name}" "${RAW}" "${output}/tool/${i}/stdout.log"; then
            STATE=error CODE=2 COUNT=null incomplete=true
            member_reason='Incomplete Geiger report; raw omissions and diagnostics retained'
        fi
        jq --arg manifest "${manifest}" --arg state "${STATE}" --arg reason "${member_reason}" --argjson code "${CODE}" --argjson raw "${RAW}" '.+[{manifest:$manifest,state:$state,exit_code:$code,tool_exit_code:$raw,reason:$reason}]' "${output}/member_results.json" >"${output}/members.next"
        mv -- "${output}/members.next" "${output}/member_results.json"
        ((final_code)) || final_code=${CODE}
        ((final_raw)) || final_raw=${RAW}
        i=$((i+1))
        jq -n --argjson completed "${i}" --argjson total "${#manifests[@]}" '{schema:1,completed:$completed,total:$total,activity:"membros"}' >"${output}/progress.next"
        mv -- "${output}/progress.next" "${output}/progress.json"
        # A cancelled supervised member must not schedule another tool.
        if ${PROCESS_CANCELLED:-false}; then exit "${RAW}"; fi
    done
    RAW=${final_raw} CODE=${final_code} STATE=recorded
    ((CODE==0)) || STATE=failed
    if ${incomplete}; then STATE=error CODE=2 REASON='Incomplete Geiger member reports; all workspace members attempted'; fi
else
    execute "${output}/tool" "${CWD}" "${CMD[@]}"
    RAW=${PROCESS_CODE}
    report=${output}/tool/stdout.log
    [[ ${name} != coverage ]] || report=${output}/coverage.lcov
    parser=${name}
    if [[ ${name} == machete ]]; then
        grep -qx '0.9.2' "${output}/version/stdout.log" || fail_check REPORT_INVALID 'Unsupported Machete version; verified text contract requires 0.9.2'
        parser=machete-text
    elif [[ ${name} == deny ]]; then
        # Transformation: JSON Lines stderr -> JSON array; raw bytes remain intact.
        report=${output}/report.json
        while IFS= read -r line; do
            printf '%s\n' "${line}" >"${output}/deny-line.json"
            # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
            strict_json "${output}/deny-line.json" || fail_check REPORT_INVALID 'Malformed/duplicate Deny JSON line'
        done <"${output}/tool/stderr.log"
        jq -s '.' "${output}/tool/stderr.log" >"${report}" || fail_check REPORT_INVALID 'Malformed Deny stream'
        [[ ! -s ${output}/tool/stdout.log ]] || fail_check REPORT_INVALID 'Unexpected Deny stdout'
    fi
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    assess "${parser}" "${RAW}" "${report}" || fail_check REPORT_INVALID 'Invalid/incomplete scanner report'
    if [[ ${name} == deny ]]; then
        jq 'group_by(.fields.code // .type)|map({code:(.[0].fields.code // .[0].type),count:length,records:.})' "${report}" >"${output}/diagnostics.json"
        [[ ${STATE} != error ]] || REASON='cargo-deny emitted internal diagnostics; inspect diagnostics.json and raw stderr'
    fi

fi
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
verify_inputs "${output}" || fail_check INPUT_INVALID 'Input/snapshot changed during check'
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
current_tool_sha=$(hash_file "${tool}") || exit 2
[[ ${current_tool_sha} == "${tool_sha}" ]] || fail_check TOOL_CHANGED 'Tool binary changed during check'
if [[ -n ${DATA} ]]; then
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    current_dataset_sha=$(tree_identity "${PREPARED}") || fail_check DATASET_INVALID 'Cannot identify dataset'
    expected_dataset_sha=$(jq -r .sha256 "${output}/dataset.json") || fail_check DATASET_INVALID 'Invalid dataset identity'
    [[ ${current_dataset_sha} == "${expected_dataset_sha}" ]] || fail_check DATASET_INVALID 'Dataset changed during check'
fi
exit 0
}
if [[ ${BASH_SOURCE[0]} == "$0" ]]; then main "$@"; fi
