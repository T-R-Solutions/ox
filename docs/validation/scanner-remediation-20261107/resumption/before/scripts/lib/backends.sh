#!/usr/bin/env bash
# Native executables and the shared-toolbox CLI are distinct trust boundaries.
# shellcheck disable=SC2034 # CMD and verdict fields are returned to checks/run.sh.
# Globals assigned by checks/run.sh; declarations preserve caller values.
declare name tool output source tool_sha TOOL
# shellcheck disable=SC2034 # BACKEND/TOOL_BIN are returned to the scanner entry.
select_backend() {
    BACKEND_REASON=''
    BACKEND=${OX_SCANNER_BACKEND:-auto}
    case $BACKEND in auto|native|toolbox) :;; *) return 1;; esac
    TOOL_BIN=''
    if [[ $BACKEND != toolbox ]]; then
        TOOL_BIN=$(command -v "$TOOL" || true)
        # Cargo plugins are global executables, not rustup components.
        if [[ -z $TOOL_BIN && $TOOL == cargo-* && -x ${CARGO_HOME:-$HOME/.cargo}/bin/$TOOL ]]; then
            TOOL_BIN=${CARGO_HOME:-$HOME/.cargo}/bin/$TOOL
        fi
        if [[ -n $TOOL_BIN ]]; then BACKEND=native; return; fi
        if [[ $BACKEND == native ]]; then
            BACKEND_REASON="executable not found: $TOOL; prepare the verified native executable explicitly or select a supported toolbox adapter"
            return 1
        fi
    fi
    case $name in ruff|gitleaks|shellcheck|grype|opengrep|osv|bandit) :;;
        *) BACKEND_REASON="required tool missing: $TOOL; Ox toolbox backend not implemented for $name; review the adapter contract before enabling it"; return 1;; esac
    BACKEND=toolbox
    if [[ ${OX_TOOLBOX_BIN+x} ]]; then
        TOOL_BIN=$OX_TOOLBOX_BIN
        [[ -n $TOOL_BIN && -f $TOOL_BIN && -x $TOOL_BIN ]] || {
            printf 'Invalid explicit OX_TOOLBOX_BIN: %s\n' "$TOOL_BIN" >&2; return 1;
        }
    else
        TOOL_BIN=$(command -v toolbox) || {
            BACKEND_REASON="required tool missing: $TOOL; toolbox CLI not found; set OX_TOOLBOX_BIN to the verified installation/bin/toolbox or expose it on PATH"
            return 1
        }
    fi
    TOOL_BIN=$(realpath -e -- "$TOOL_BIN") || return 1
    local installation
    installation=$(dirname -- "$(dirname -- "$TOOL_BIN")")
    [[ -f $TOOL_BIN && -x $TOOL_BIN && $TOOL_BIN == "$installation/bin/toolbox" &&
       -f $installation/toolbox/cli.py && -f $installation/toolbox/__init__.py ]] || {
        printf 'Invalid toolbox installation contract: %s\n' "$TOOL_BIN" >&2; return 1;
    }
}
backend_plan() {
    local native=$1
    if select_backend; then
        if [[ $BACKEND == toolbox ]]; then
            CMD=("$TOOL_BIN" run --config '{runtime-toolbox.json}' --only "$name")
        fi
    else BACKEND=unavailable; TOOL_BIN=$native; fi
}
run_toolbox() {
    local config lock spec result report raw status expected runner_code library_sha toolbox_root
    local scanner=$name
    [[ $name != osv ]] || scanner=osv-scanner
    if ! config=$(contained scripts/config/toolbox.json) || [[ ! -f $config ]]; then
        fail_check 'Missing scripts/config/toolbox.json'
    fi
    if ! lock=$(contained scripts/config/toolbox.images.lock.json) || [[ ! -f $lock ]]; then
        fail_check 'Missing toolbox image lock; explicit shared-toolbox prepare required'
    fi
    if ! strict_json "$config" || ! strict_json "$lock"; then
        fail_check 'Invalid/duplicate toolbox config or image lock'
    fi
    spec=$(jq -ce --arg name "$scanner" '.tools[$name] | select(type=="object" and (.enabled!=false) and (.applicable!=false) and .network=="none" and .timeout>0 and .timeout<=600)' "$config") || fail_check 'Toolbox selection is omitted, inapplicable or violates offline/timeout policy'
    jq -e --arg name "$scanner" --argjson spec "$spec" '.schema==1 and (.tools[$name] | .version==$spec.version and (.id|test("^sha256:[0-9a-f]{64}$")) and (.adapter_sha256|test("^[0-9a-f]{64}$")))' "$lock" >/dev/null || fail_check 'Missing/inconsistent immutable toolbox image identity'
    toolbox_root=$(dirname -- "$(dirname -- "$tool")")
    library_sha=$(tree_identity "$toolbox_root/toolbox") || fail_check 'Cannot identify shared-toolbox library'
    jq -n --arg path "$toolbox_root/toolbox" --arg sha "$library_sha" '{path:$path,sha256:$sha}' >"$output/backend_inputs.json"
    input_add "$output" scripts/config/toolbox.json
    input_add "$output" scripts/config/toolbox.images.lock.json
    # The same prepared image lock is valid when the identified source root moves.
    jq --arg root "$source" --arg name "$scanner" '.root=$root | .tools={($name):.tools[$name]}' "$config" >"$output/toolbox.json"
    if [[ $name == ruff || $name == bandit || $name == shellcheck ]]; then
        # Explicit per-file argv prevents discovery defaults from omitting inputs.
        jq --arg name "$scanner" --argjson spec "$spec" --slurpfile inputs "$output/inputs.json" '
          .tools[$name].paths=[$inputs[0]|keys[]|. as $p|
            select(if $name=="shellcheck" then startswith("scripts/") and endswith(".sh")
              else endswith(".py") and any($spec.paths[]; . as $dir|$dir=="." or $p==$dir or ($p|startswith($dir+"/"))) end)] |
          if (.tools[$name].paths|length)>0 then . else error("empty scanner input selection") end' "$output/toolbox.json" >"$output/toolbox.next.json" || fail_check 'Empty/incomplete scanner file selection'
        mv -- "$output/toolbox.next.json" "$output/toolbox.json"
    fi
    cp -- "$lock" "$output/toolbox.images.lock.json"
    # The candidate Ruff adapter has no ignore-noqa switch. Refuse suppressions.
    if [[ $name == ruff ]] && grep -REin '#[[:space:]]*no[q]a' "$source" --include='*.py' >"$output/suppressions.log"; then
        fail_check 'Toolbox Ruff inline suppression requires review; use strict native adapter'
    fi
    if [[ $name == gitleaks ]] && grep -RIln 'gitleaks:[a]llow' "$source" >"$output/suppressions.log"; then
        fail_check 'Toolbox Gitleaks inline suppression requires review; use strict native adapter'
    fi
    # Only generated per-run snapshots and outputs are relabeled by the toolbox.
    export TOOLBOX_SELINUX_LABEL=private
    EXECUTED=true
    execute "$output/toolbox" "$ROOT" "$tool" run --config "$output/toolbox.json" --only "$scanner"
    runner_code=$PROCESS_CODE RUNNER_RAW=$PROCESS_CODE
    strict_json "$output/toolbox/stdout.log" || fail_check 'Invalid toolbox summary'
    raw=$(jq -r '.tools[0].tool_exit_code | select(type=="number" and floor==. and .>=0 and .<=255)' "$output/toolbox/stdout.log") || fail_check 'Invalid toolbox exit field'
    [[ -z $raw ]] || RAW=$raw
    jq -e --arg name "$scanner" --argjson code "$runner_code" '
      .schema==1 and .project=="ox" and .sources_unchanged==true and (.cancelled//false|not) and
      (.tools|type=="array" and length==1) and .tools[0].tool==$name and
      (.tools[0].status as $s | if $s=="success" then $code==0 elif $s=="findings" then $code==1 else false end) and
      (.tools[0] | .timed_out==false and .cancelled==false and .runtime_error==null and
        (.tool_exit_code|type=="number"))' "$output/toolbox/stdout.log" >/dev/null || fail_check "Toolbox failed, omitted, incomplete or exit/status disagreement: $(jq -r '.tools[0].reason // .error // "inspect toolbox/stdout.log and toolbox/stderr.log"' "$output/toolbox/stdout.log")"
    result=$(jq -r '.tools[0].output' "$output/toolbox/stdout.log")
    # The trusted external CLI owns its volume paths; never follow report symlinks.
    local path
    [[ $result == "$toolbox_root/tools/$scanner/volume/projects/ox/runs/"* && $result != *'/../'* ]] || fail_check 'Toolbox report escaped expected volume'
    for path in "$result" "$result/stdout.log" "$result/stderr.log"; do
        [[ ! -L $path && $(realpath -e -- "$path") == "$path" ]] || fail_check 'Symlinked/missing toolbox report'
    done
    mkdir -- "$output/tool"
    cp -- "$result/stdout.log" "$result/stderr.log" "$output/tool/"
    RAW=$(jq -r '.tools[0].tool_exit_code' "$output/toolbox/stdout.log")
    status=$(jq -r '.tools[0].status' "$output/toolbox/stdout.log")
    report=$output/tool/stdout.log
    expected=1
    if [[ $name == gitleaks ]]; then
        [[ -f $result/native.json && ! -L $result/native.json ]] || fail_check 'Missing Gitleaks native report'
        cp -- "$result/native.json" "$output/report.json"; report=$output/report.json; expected=42
    elif [[ $name == shellcheck ]]; then
        if ! strict_json "$report" || ! jq -e '.comments|type=="array"' "$report" >/dev/null; then
            fail_check 'Incomplete ShellCheck json1'
        fi
        jq '.comments' "$report" >"$output/report.json"; report=$output/report.json
    elif [[ $name == grype ]]; then expected=0; fi
    COUNT=$(finding_count "$name" "$report") || { COUNT=null; fail_check 'Invalid native toolbox scanner report'; }
    [[ ( $status == success && $COUNT == 0 && $RAW == 0 ) ||
       ( $status == findings && $COUNT -gt 0 && $RAW == "$expected" ) ]] || fail_check 'Native report and toolbox verdict disagree'
    STATE=passed CODE=0
    if ((COUNT)); then STATE=findings CODE=1; fi
    if [[ $name == opengrep ]]; then
        jq -e --slurpfile inputs "$output/inputs.json" '.paths.scanned as $scanned |
          all($inputs[0]|keys[]|select(test("\\.(rs|py)$")); . as $p |
            ($scanned|index("/src/"+$p))!=null)' "$report" >/dev/null || fail_check 'SAST omitted selected source inputs'
    fi
    if [[ $name == bandit ]]; then
        jq -e --argjson spec "$spec" --slurpfile inputs "$output/inputs.json" '.metrics as $metrics |
          all($inputs[0]|keys[]|select(endswith(".py")); . as $p |
            if any($spec.paths[]; . as $dir | $dir=="." or $p==$dir or ($p|startswith($dir+"/")))
            then ($metrics|has("/src/"+$p)) else true end)' "$report" >/dev/null || fail_check 'Bandit omitted selected Python inputs'
    fi
    # Preserve full external record with image/database/command/exit identities.
    cp -- "$output/toolbox/stdout.log" "$output/backend_record.json"
    verify_inputs "$output" || fail_check 'Input/snapshot changed during toolbox check'
    [[ $(hash_file "$tool") == "$tool_sha" && $(tree_identity "$toolbox_root/toolbox") == "$library_sha" ]] || fail_check 'Toolbox code changed during check' 
}
