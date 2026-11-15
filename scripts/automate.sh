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
if ! ${legacy}; then execution_environment; fi
run=$(new_run run)
run_lease "${run}"
trap 'rc=$?; run_complete "$run" || exit 2; exit "$rc"' EXIT
printf '[]\n' >"${run}/results.rows.json"
toolchain_code=0
if ${needs_cargo}; then
    mkdir -- "${run}/toolchain"
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    if installed_cargo >"${run}/toolchain/stdout.log" 2>"${run}/toolchain/stderr.log"; then toolchain_code=0
    else toolchain_code=$?; fi
    cat "${run}/toolchain/stderr.log" >&2
fi
for name in "${selected[@]}"; do
    d=${run}/${name}
    # shellcheck disable=SC2310 # check_properties is an explicit status predicate.
    if [[ ${name} == rust-* && ${toolchain_code} != 0 ]]; then
        check_command "${name}" "${d}"
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
    omitted:[$base[] as $n|select($selected|index($n)|not)|{check:$n,reason:"not selected by --check; applicability must be recorded by the task"}],
    not_selected:["Surfaces outside the chosen scope need explicit applicability review"],not_applicable:[],
    manual_evidence:["Graphical X11/Wayland acceptance: separate applicable protocol required"],
    limits:["Successful checks do not approve the product.","Offline flags are not OS isolation."]}' >"${run}/results.json"
printf 'Logs: %s/logs\n' "${ROOT}/.local"
if ${legacy}; then
    aggregate_code=$(jq -r '[.results[].exit_code|select(.!=0)][0]//0' "${run}/results.json") || exit 2
exit "${aggregate_code}"
fi
# Same aggregate precedence as Ec: errors, blocked prerequisites, findings, pass.
aggregate_code=$(jq -r '
  if any(.results[]; .state=="error" or
      (.state!="blocked" and .exit_code!=0 and .exit_code!=1 and .exit_code!=3)) then 2
  elif any(.results[]; .state=="blocked" or .exit_code==3) then 3
  elif any(.results[]; .exit_code!=0) then 1 else 0 end' "${run}/results.json") || exit 2
exit "${aggregate_code}"
