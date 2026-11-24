#!/usr/bin/env bash
# shellcheck disable=SC2154 # ROOT is initialized by common.sh before loading this module.
# shellcheck disable=SC2034 # PROCESS_CODE is the caller-visible process result.
# Run argv without a shell interpreter, capture raw streams, replay after exit.
execute() {
    local directory=$1 cwd=$2
    shift 2
    mkdir -- "${directory}"
    local rc=0 child_code=0 state=passed human_progress=false
    local child signal_received=false cancelled=false received_signal='' saved_traps depth=${OX_EXECUTE_DEPTH:-0}
    saved_traps=$(trap -p INT TERM HUP)
    PROCESS_CANCELLED=false
    PROCESS_SIGNAL_CODE=0
    # An inherited presentation flag must not create an unsupervised child when
    # the standalone consumer has not loaded the presentation callbacks.
    if [[ ${OX_HUMAN_PROGRESS:-false} == true && ${depth} == 0 ]] &&
       declare -F progress_watch_start >/dev/null && declare -F progress_watch_stop >/dev/null; then
        human_progress=true
    fi
    # Without job control, Bash starts asynchronous lists with SIGINT/SIGQUIT
    # ignored, and an ignored-on-entry signal cannot be trapped by a nested
    # shell. Restore the dispositions inherited by this shell before exec.
    (trap - INT QUIT; export OX_EXECUTE_DEPTH=$((depth+1)); cd -- "${cwd}" && exec "$@") </dev/null >"${directory}/stdout.log" 2>"${directory}/stderr.log" &
    child=$!
    # Forward cancellation; wait through the executor's own cleanup, without a
    # competing outer timeout. Never signal other executions or process groups.
    trap 'signal_received=true; cancelled=true; received_signal=INT; kill -TERM "$child" 2>/dev/null || true' INT
    trap 'signal_received=true; cancelled=true; received_signal=TERM; kill -TERM "$child" 2>/dev/null || true' TERM
    trap 'signal_received=true; cancelled=true; received_signal=HUP; kill -TERM "$child" 2>/dev/null || true' HUP
    if ${human_progress}; then progress_watch_start "${child}"; fi
    while true; do
        rc=0
        wait "${child}" || rc=$?
        if ${signal_received} && kill -0 "${child}" 2>/dev/null; then
            signal_received=false
            continue
        fi
        break
    done
    trap - INT TERM HUP
    [[ -z ${saved_traps} ]] || eval "${saved_traps}"
    if ${human_progress}; then progress_watch_stop
    else
        cat -- "${directory}/stdout.log"
        cat -- "${directory}/stderr.log" >&2
    fi
    child_code=${rc}
    if ${cancelled}; then
        case ${received_signal} in INT) rc=130;; TERM) rc=143;; HUP) rc=129;; *) rc=2;; esac
        PROCESS_SIGNAL_CODE=${rc}
    fi
    if ((rc==126 || rc==127)); then state=blocked
    elif ((rc)); then state=failed; fi
    jq -n --arg cwd "${cwd}" --arg state "${state}" --argjson code "${rc}" --argjson child_code "${child_code}" --argjson cancelled "${cancelled}" --arg signal "${received_signal}" \
       '{argv_recorded:false,cwd:$cwd,exit_code:$code,state:$state} + (if $cancelled then {cancelled:true,signal:$signal,child_exit_code:$child_code} else {} end)' >"${directory}/process.json"
    PROCESS_CODE=${rc}
    PROCESS_CANCELLED=${cancelled}
}

installed_cargo() {
    local channel cargo
    [[ -f ${ROOT}/application/rust-toolchain.toml ]] || return 1
    # Read only the pinned channel assignment; Cargo parses the workspace TOML.
    channel=$(sed -nE 's/^[[:space:]]*channel[[:space:]]*=[[:space:]]*"([^"]+)"[[:space:]]*(#.*)?$/\1/p' "${ROOT}/application/rust-toolchain.toml") || return 1
    [[ -n ${channel} && ${channel} != *$'\n'* ]] || return 1
    cargo=$(rustup which --toolchain "${channel}" cargo) || return
    [[ ${cargo} == /* && -f ${cargo} && -x ${cargo} ]] || return 1
    export CARGO=${cargo} RUSTUP_TOOLCHAIN=${channel} PATH="${cargo%/*}:${PATH}"
}
workspace_metadata() {
    (cd -- "${ROOT}/application" && "${CARGO}" metadata --no-deps --all-features --format-version 1 --locked --offline)
}

# Validate the actual Cargo metadata manifest before mapping it to a snapshot.
validate_member_manifest() {
    local manifest=$1 checked
    [[ ${manifest} == "${ROOT}/application/"* ]] || return 1
    checked=$(contained "${manifest#"${ROOT}/"}") || return 1
    [[ -f ${checked} && ${checked##*/} == Cargo.toml ]]
}
