#!/usr/bin/env bash
if [[ ${BASH_SOURCE[0]} != "$0" ]]; then
    printf 'Execute automate.sh with bash or ./scripts/automate.sh; do not source it.\n' >&2
    return 2
fi
# Public task closure entry. Bash 4.4+, jq 1.6+, GNU coreutils/find.
# shellcheck source=lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/lib/common.sh"
# shellcheck source=lib/process.sh
source "${LIB_DIR}/process.sh"
# shellcheck source=lib/registry.sh
source "${LIB_DIR}/registry.sh"
# shellcheck source=lib/backends.sh
source "${LIB_DIR}/backends.sh"
usage() {
    cat <<'HELP'
Usage: ./scripts/automate.sh plan|run [--root PATH] [--scope complete] [--surface NAME] [--check NAME]
Surfaces: docs scripts application security (default: all).
complete includes Grype, Bandit, Syft and YARA-X; it cannot be combined with filters.
--surface and --check are repeatable; docs/governance remains mandatory.
coverage requires an explicit --surface application.
plan emits JSON without executing checks or preparing resources.
Legacy: --scope governance|rust|security|quality|full|complete [--check NAME] [--plan].
HELP
}
main() {
scope='' plan=false legacy=false scope_seen=false
requested=() requested_surfaces=() OPTIONAL=()
(($#)) || { usage >&2; exit 2; }
case $1 in
    plan) plan=true; scope=default; shift;;
    run) scope=default; shift;;
    -h|--help) usage; exit 0;;
    --scope|--root|--check|--plan) legacy=true;;
    *) die 'Operation must be plan or run';;
esac
while (($#)); do
    case $1 in
        --scope|--root|--check|--surface)
            (($#>=2)) && [[ -n $2 && $2 != --* ]] || die "Missing value: $1"
            case $1 in
                --scope)
                    ! ${scope_seen} || die 'Repeated --scope'
                    ${legacy} || [[ $2 == complete ]] || die "Unknown scope: $2"
                    scope=$2; scope_seen=true;;
                --root) ROOT=$2;;
                --check) requested+=("$2");;
                --surface) ! ${legacy} || die '--surface requires plan or run'; requested_surfaces+=("$2");;
                *) :;; # Other validated classifications require no action.
            esac
            shift 2;;
        --plan) ${legacy} || die 'Use the plan operation'; plan=true; shift;;
        --help|-h) usage; exit 0;;
        *) die "Unknown argument: $1";;
    esac
done
ROOT=$(cd -- "${ROOT}" && pwd -P) || die 'Repository root missing'
if ! ${legacy} && [[ ${scope} == complete ]] && ((${#requested[@]} + ${#requested_surfaces[@]})); then
    die '--scope complete cannot be combined with --surface or --check'
fi
if ${legacy}; then scope_checks "${scope}"; else catalog_load; fi
GROUP=all
if ${legacy} && [[ ${scope} != full && ${scope} != complete ]]; then GROUP=fast; fi
for rel in AGENTS.md sdd/tools/validate.py tools/governance/scripts/check-ox.py tools/governance/scripts/run-tests.py; do
    [[ -f ${ROOT}/${rel} ]] || die "Missing Ox input: ${rel}"
done
if ${legacy}; then
# shellcheck disable=SC2154 # scope_checks assigns BASE through the shared catalog contract.
selected=("${BASE[@]}")
available=("${BASE[@]}")
case ${scope} in security|quality|full) available+=("${OPTIONAL[@]}");; *) :;; esac
if ((${#requested[@]})); then
    selected=()
    for name in "${requested[@]}"; do
        found=false
        for candidate in "${available[@]}"; do [[ ${name} != "${candidate}" ]] || found=true; done
        ${found} || die "Unknown check selection: ${name}"
    done
    for name in "${available[@]}"; do
        for candidate in "${requested[@]}"; do
            if [[ ${name} == "${candidate}" ]]; then selected+=("${name}"); break; fi
        done
    done
fi
else
    # shellcheck source=lib/selection.sh
    source "${LIB_DIR}/selection.sh"
    select_checks
fi
needs_cargo=false
for name in "${selected[@]}"; do
    case ${name} in rust-*|audit|deny|machete|coverage|geiger) needs_cargo=true;; *) :;; esac
done
if ${needs_cargo}; then
    [[ -f ${ROOT}/application/Cargo.lock ]] || die 'Cargo.lock missing'

fi
if ${plan}; then
    for name in "${selected[@]}"; do
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        if check_properties "${name}"; then backend_plan
        else check_command "${name}" '{output}'; fi
        # Keep paths relative in plan cwd for compatibility with consumers.
        cwd=${CWD#"${ROOT}"}; cwd=${cwd#/}; cwd=${cwd:-.}
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        argv_json=$(json_args "${CMD[@]}") || exit 2
        jq -cn --arg name "${name}" --arg cwd "${cwd}" --argjson argv "${argv_json}" '[$name,$cwd,$argv]'
    done | jq -s .
    exit 0
fi
# Capture the operator preference before scanner defaults set NO_COLOR.
PROGRESS_USER_NO_COLOR=${NO_COLOR:-}
# Both interfaces retain their selection semantics and share execution defaults.
# shellcheck source=lib/selection.sh
source "${LIB_DIR}/selection.sh"
execution_environment
# shellcheck source=lib/progress.sh
source "${LIB_DIR}/progress.sh"
run=$(new_run run)
# Own cleanup immediately, including lease/presentation setup failure.
trap 'rc=$?; rm -rf -- "${run}"; exit "$rc"' EXIT
run_lease "${run}"
progress_init "${run}" "${#selected[@]}"
# shellcheck source=lib/lifecycle.sh
source "${LIB_DIR}/lifecycle.sh"
trap 'finalize_run "$?"' EXIT
trap 'PROGRESS_CANCELLED=true; exit 130' INT
trap 'PROGRESS_CANCELLED=true; exit 143' TERM
trap 'PROGRESS_CANCELLED=true; exit 129' HUP
progress_begin preparation
printf '[]\n' >"${run}/results.rows.json"
toolchain_code=0
if ${needs_cargo}; then
    mkdir -- "${run}/toolchain"
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    if installed_cargo >"${run}/toolchain/stdout.log" 2>"${run}/toolchain/stderr.log"; then toolchain_code=0
    else toolchain_code=$?; fi
fi
mkdir -- "${run}/preparation"
jq -n --argjson code "${toolchain_code}" '{exit_code:$code,state:(if $code==0 then "passed" else "blocked" end),reason:(if $code==0 then "" else "Required installed toolchain unavailable" end)}' >"${run}/preparation/result.json"
progress_end "${run}/preparation/result.json"
for name in "${selected[@]}"; do
    d=${run}/${name}
    progress_begin "${name}" "${d}"
    PROCESS_CANCELLED=false
    # shellcheck disable=SC2310 # check_properties is an explicit status predicate.
    if [[ ${name} == rust-* && ${toolchain_code} != 0 ]]; then
        mkdir -- "${d}"
        jq -n --arg check "${name}" --argjson code "${toolchain_code}" \
          '{check:$check,argv_recorded:false,exit_code:$code,state:"blocked",reason:"Required installed toolchain unavailable"}' >"${d}/process.json"
    elif check_properties "${name}"; then
        execute "${d}" "${ROOT}" bash "${SCRIPTS_DIR}/checks/run.sh" --root "${ROOT}" --check "${name}" --output "${d}"
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        if [[ -f ${d}/assessment.json ]] && strict_json "${d}/assessment.json" && \
           jq -e --argjson code "${PROCESS_CODE}" '.exit_code==$code' "${d}/assessment.json" >/dev/null; then
            jq --slurpfile a "${d}/assessment.json" '. + ($a[0]|{state,tool_exit_code})' "${d}/process.json" >"${d}/merged.json"
        else
            jq '. + {state:"error",reason:"Missing/invalid adapter assessment"} | if .exit_code==0 then .exit_code=2 else . end' "${d}/process.json" >"${d}/merged.json"
        fi
        mv -- "${d}/merged.json" "${d}/process.json"
    else
        check_command "${name}" "${d}"
        execute "${d}" "${CWD}" "${CMD[@]}"
    fi
    jq --arg check "${name}" '.+{check:$check}' "${d}/process.json" >"${d}/result.json"
    jq --slurpfile row "${d}/result.json" '.+[$row[0]]' "${run}/results.rows.json" >"${run}/results.next"
    mv -- "${run}/results.next" "${run}/results.rows.json"
    progress_end "${d}/result.json" "${d}/assessment.json"
    if ${PROGRESS_CANCELLED}; then break; fi
done
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
base_json=$(json_args "${BASE[@]}") || exit 2
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
selected_json=$(json_args "${selected[@]}") || exit 2
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
entry_sha=$(hash_file "${BASH_SOURCE[0]}") || exit 2
jq -n --arg scope "${scope}" --slurpfile results "${run}/results.rows.json" \
  --argjson base "${base_json}" --argjson selected "${selected_json}" --arg hash "${entry_sha}" \
  '{scope:$scope,results:$results[0],product_acceptance:false,entry_sha256:$hash,
    omitted:[$base[] as $n|select($selected|index($n)|not)|{check:$n,reason:"not selected by scope/check filter; applicability must be recorded by the task"}],
    not_selected:["Surfaces outside the chosen scope need explicit applicability review"],not_applicable:[],
    manual_evidence:["Graphical X11/Wayland acceptance: separate applicable protocol required"],
    limits:["Successful checks do not approve the product.","Offline flags are not OS isolation."]}' >"${run}/results.json"
# shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
aggregate_code=$(aggregate_results "${run}/results.json") || exit 2
exit "${aggregate_code}"
}
main "$@"
