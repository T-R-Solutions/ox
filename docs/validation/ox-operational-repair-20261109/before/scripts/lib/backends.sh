#!/usr/bin/env bash
# Central catalog transport. Cargo utilities remain explicit local product tools.
select_backend() {
    BACKEND_REASON='' TOOL_BIN=''
    if [[ ${OX_TOOLBOX_BIN+x} || ${OX_SCANNER_BACKEND+x} ]]; then
        BACKEND_REASON='Obsolete OX_TOOLBOX_BIN/OX_SCANNER_BACKEND; remove them and use TOOLBOX_BIN or PATH'
        return 1
    fi
    case $name in
        audit|deny|machete|coverage|geiger)
            BACKEND=native
            TOOL_BIN=$(command -v "$TOOL" || true)
            if [[ -z $TOOL_BIN && -x ${CARGO_HOME:-$HOME/.cargo}/bin/$TOOL ]]; then
                TOOL_BIN=${CARGO_HOME:-$HOME/.cargo}/bin/$TOOL
            fi
            [[ -n $TOOL_BIN ]] || { BACKEND_REASON="Required local Cargo utility unavailable: $TOOL (outside central catalog)"; return 1; };;
        *) BACKEND=toolbox; TOOL_BIN=$LIB_DIR/../toolbox.sh;;
    esac
}
backend_plan() {
    CMD=() CWD=$ROOT
    select_backend || { BACKEND=unavailable; return; }
    if [[ $BACKEND == toolbox ]]; then
        native_command '{source}'
        CMD=("$TOOL_BIN" exec --tool "$SCANNER" --project-root '{source}' --results '{output}' --timeout 600 --diagnostic-file '{output}/backend_record.json' -- "${NATIVE[@]}")
    else
        check_command "$name" '{output}'
    fi
}
run_toolbox() {
    local report before
    [[ -z $CONFIG || -f $source/scripts/config/$CONFIG ]] || fail_check 'Missing native configuration'
    [[ -z $RULE || -f $source/scripts/security/rules/$RULE ]] || fail_check 'Missing native rules'
    native_command "$source"
    before=$(tree_identity "$source") || fail_check 'Cannot identify complete snapshot'
    EXECUTED=true
    execute "$output/tool" "$ROOT" "$tool" exec --tool "$SCANNER" --project-root "$source" \
        --results "$output" --timeout 600 --diagnostic-file "$output/backend_record.json" -- "${NATIVE[@]}"
    RUNNER_RAW=$PROCESS_CODE
    strict_json "$output/backend_record.json" || fail_check 'Missing/invalid native execution diagnostic'
    RAW=$(jq -er 'if .native_exit_code==null then "null" elif (.native_exit_code|type)=="number" and (.native_exit_code|floor)==.native_exit_code and .native_exit_code>=0 and .native_exit_code<=255 then .native_exit_code else error("invalid native exit") end' "$output/backend_record.json") || { RAW=null; fail_check 'Invalid diagnostic native exit'; }
    jq -e --arg tool "$SCANNER" --argjson code "$PROCESS_CODE" '
        .tool==$tool and .outcome=="native" and .cleanup=="removed" and
        (.version|type=="string" and length>0) and (.image|test("^sha256:[0-9a-f]{64}$")) and
        (.native_exit_code|type=="number" and floor==. and .>=0 and .<=255) and .native_exit_code==$code
    ' "$output/backend_record.json" >/dev/null || fail_check 'Executor infrastructure, timeout, cancellation, cleanup or identity failure; inspect diagnostic'
    case $name in
        osv|trivy)
            validate_database_age "$output/backend_record.json" "$name" || fail_check 'Invalid, inconsistent or expired central database metadata';;
        grype)
            jq -e '.database|type=="string" and test("^[0-9a-f]{64}$")' "$output/backend_record.json" >/dev/null || fail_check 'Missing central database identity';;
    esac
    report=$output/tool/stdout.log
    [[ $name != gitleaks && $name != history ]] || report=$output/report.json
    assess "$name" "$RAW" "$report" || fail_check 'Invalid/incomplete native report'
    # For native scanners, a clean report must have exit zero; findings must agree
    # with the chosen native exit policy (Grype/YARA return zero with findings).
    local expected=1
    case $name in gitleaks|history) expected=10;; grype|malware) expected=0;; esac
    [[ ( $COUNT == 0 && $RAW == 0 ) || ( $COUNT -gt 0 && $RAW == "$expected" ) ]] || fail_check 'Native findings and exit disagree'
    if ((COUNT>0)); then STATE=findings CODE=1; fi
    if [[ $name == opengrep ]]; then
        jq -e --slurpfile inputs "$output/inputs.json" '.paths.scanned as $scanned |
          all($inputs[0]|keys[]|select(test("\\.(rs|py)$")); . as $p | ($scanned|index("/project/"+$p))!=null)' "$report" >/dev/null || fail_check 'SAST omitted selected input'
    fi
    if [[ $name == bandit ]]; then
        jq -e --slurpfile inputs "$output/inputs.json" '.metrics as $metrics |
          all($inputs[0]|keys[]|select(endswith(".py")); . as $p | $metrics|has("/project/"+$p))' "$report" >/dev/null || fail_check 'Bandit omitted selected input'
    fi
    [[ $(tree_identity "$source") == "$before" ]] && verify_inputs "$output" || fail_check 'Input/snapshot changed'
    mkdir -- "$output/recheck"
    source_snapshot "$output/recheck" all || fail_check 'Cannot verify final source selection'
    cmp -s -- "$output/inputs.json" "$output/recheck/inputs.json" &&
        cmp -s -- "$output/input_modes.json" "$output/recheck/input_modes.json" || fail_check 'Source inventory or modes changed during scan'
    [[ $(hash_file "$tool") == "$tool_sha" ]] || fail_check 'Wrapper changed during check'
}

# Consumer age policy; timestamps identify upstream data, never local preparation.
validate_database_age() {
    local record=$1 age_policy=$2 limit=86400 oldest=9223372036854775807 value epoch effective current
    [[ $age_policy == osv ]] || limit=432000
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
          .timestamp_semantics=="native_database_updated_at")))' "$record" >/dev/null || return 1
    current=$(date -u +%s)
    local -a timestamps
    mapfile -t timestamps < <(jq -r '.database_metadata.sources[].data_timestamp' "$record")
    for value in "${timestamps[@]}"; do
        [[ $value =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})$ ]] || return 1
        epoch=$(date -ud "$value" +%s) || return 1
        ((epoch<=current && current-epoch<=limit)) || return 1
        ((epoch>=oldest)) || oldest=$epoch
    done
    value=$(jq -r '.database_metadata.data_timestamp' "$record")
    effective=$(date -ud "$value" +%s) || return 1
    ((effective==oldest))
}
