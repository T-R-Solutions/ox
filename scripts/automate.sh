#!/usr/bin/env bash
# Public task closure entry. Bash 4.4+, jq 1.6+, GNU coreutils/find.
# shellcheck source=lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/lib/common.sh"
# shellcheck source=lib/process.sh
source "$LIB_DIR/process.sh"
# shellcheck source=lib/registry.sh
source "$LIB_DIR/registry.sh"
# shellcheck source=lib/backends.sh
source "$LIB_DIR/backends.sh"
scope='' plan=false
requested=()
while (($#)); do
    case $1 in
        --scope|--root|--check)
            (($#>=2)) || die "Missing value: $1"
            case $1 in --scope) scope=$2;; --root) ROOT=$2;; --check) requested+=("$2");; esac
            shift 2;;
        --plan) plan=true; shift;;
        --help|-h) printf 'Usage: automate.sh --scope governance|rust|security|quality|full [--check NAME] [--root PATH] [--plan]\n'; exit 0;;
        *) die "Unknown argument: $1";;
    esac
done
ROOT=$(cd -- "$ROOT" && pwd -P) || die 'Repository root missing'
scope_checks "$scope"
GROUP=fast; [[ $scope != full ]] || GROUP=all
for rel in AGENTS.md sdd/tools/validate.py tools/governance/scripts/check-ox.py tools/governance/scripts/run-tests.py; do
    [[ -f $ROOT/$rel ]] || die "Missing Ox input: $rel"
done
selected=("${BASE[@]}")
available=("${BASE[@]}")
case $scope in security|quality|full) available+=("${OPTIONAL[@]}");; esac
if ((${#requested[@]})); then
    selected=()
    for name in "${requested[@]}"; do
        found=false
        for candidate in "${available[@]}"; do [[ $name != "$candidate" ]] || found=true; done
        $found || die "Unknown check selection: $name"
    done
    for name in "${available[@]}"; do
        for candidate in "${requested[@]}"; do
            if [[ $name == "$candidate" ]]; then selected+=("$name"); break; fi
        done
    done
fi
if [[ $scope == rust || $scope == full ]]; then
    [[ -f $ROOT/application/Cargo.lock ]] || die 'Cargo.lock missing'
    if $plan; then
        installed_cargo || die 'Required installed toolchain unavailable'
        metadata=$(workspace_metadata) || die 'Invalid Cargo workspace'
        jq -e --arg root "$ROOT/application" '.workspace_root==$root and .resolve==null' <<<"$metadata" >/dev/null || die 'Invalid workspace metadata'
        # A virtual workspace has no root package manifest among its members.
        jq -e --arg manifest "$ROOT/application/Cargo.toml" 'all(.packages[];.manifest_path!=$manifest)' <<<"$metadata" >/dev/null || die 'Expected virtual workspace'
    fi
fi
if $plan; then
    for name in "${selected[@]}"; do
        if check_properties "$name"; then backend_plan
        else check_command "$name" '{output}'; fi
        # Keep paths relative in plan cwd for compatibility with consumers.
        cwd=${CWD#"$ROOT"}; cwd=${cwd#/}; cwd=${cwd:-.}
        jq -cn --arg name "$name" --arg cwd "$cwd" --argjson argv "$(json_args "${CMD[@]}")" '[$name,$cwd,$argv]'
    done | jq -s .
    exit 0
fi
run=$(new_run run)
printf '[]\n' >"$run/results.rows.json"
toolchain_code=0
if [[ $scope == rust || $scope == full ]]; then
    mkdir -- "$run/toolchain"
    if installed_cargo >"$run/toolchain/stdout.log" 2>"$run/toolchain/stderr.log"; then toolchain_code=0
    else toolchain_code=$?; fi
    cat "$run/toolchain/stderr.log" >&2
fi
for name in "${selected[@]}"; do
    d=$run/$name
    if [[ $name == rust-* && $toolchain_code != 0 ]]; then
        check_command "$name" "$d"
        mkdir -- "$d"
        jq -n --arg check "$name" --argjson code "$toolchain_code" \
          '{check:$check,argv_recorded:false,exit_code:$code,state:"blocked",reason:"Required installed toolchain unavailable"}' >"$d/process.json"
    elif check_properties "$name"; then
        execute "$d" "$ROOT" bash "$SCRIPTS_DIR/checks/run.sh" --root "$ROOT" --check "$name" --output "$d"
        if [[ -f $d/assessment.json ]] && strict_json "$d/assessment.json" && \
           jq -e --argjson code "$PROCESS_CODE" '.exit_code==$code' "$d/assessment.json" >/dev/null; then
            jq --slurpfile a "$d/assessment.json" '. + ($a[0]|{state,tool_exit_code})' "$d/process.json" >"$d/merged.json"
        else
            jq '. + {state:"error",reason:"Missing/invalid adapter assessment"} | if .exit_code==0 then .exit_code=2 else . end' "$d/process.json" >"$d/merged.json"
        fi
        mv -- "$d/merged.json" "$d/process.json"
    else
        check_command "$name" "$d"
        execute "$d" "$CWD" "${CMD[@]}"
    fi
    jq --arg check "$name" '.+{check:$check}' "$d/process.json" >"$d/result.json"
    jq --slurpfile row "$d/result.json" '.+[$row[0]]' "$run/results.rows.json" >"$run/results.next"
    mv -- "$run/results.next" "$run/results.rows.json"
done
jq -n --arg scope "$scope" --slurpfile results "$run/results.rows.json" \
  --argjson base "$(json_args "${BASE[@]}")" --argjson selected "$(json_args "${selected[@]}")" --arg hash "$(hash_file "${BASH_SOURCE[0]}")" \
  '{scope:$scope,results:$results[0],product_acceptance:false,entry_sha256:$hash,
    omitted:[$base[] as $n|select($selected|index($n)|not)|{check:$n,reason:"not selected by --check; applicability must be recorded by the task"}],
    not_selected:["Surfaces outside the chosen scope need explicit applicability review"],not_applicable:[],
    manual_evidence:["Graphical X11/Wayland acceptance: separate applicable protocol required"],
    limits:["Successful checks do not approve the product.","Offline flags are not OS isolation."]}' >"$run/results.json"
printf 'Check records: %s\n' "$run"
exit "$(jq -r '[.results[].exit_code|select(.!=0)][0]//0' "$run/results.json")"
