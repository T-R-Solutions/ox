#!/usr/bin/env bash
# shellcheck disable=SC2154 # ROOT is initialized by common.sh before loading this module.
# shellcheck disable=SC2034 # PROCESS_CODE is the caller-visible process result.
# Run argv without a shell interpreter, capture raw streams, replay after exit.
execute() {
    local directory=$1 cwd=$2
    shift 2
    mkdir -- "${directory}"
    local rc=0 state=passed
    local child signal_received=false
    (cd -- "${cwd}" && exec "$@") </dev/null >"${directory}/stdout.log" 2>"${directory}/stderr.log" &
    child=$!
    # Forward cancellation; wait through the executor's own cleanup, without a
    # competing outer timeout. Never signal other executions or process groups.
    trap 'signal_received=true; kill -TERM "$child" 2>/dev/null || true' INT TERM HUP
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
    cat -- "${directory}/stdout.log"
    cat -- "${directory}/stderr.log" >&2
    if ((rc==126 || rc==127)); then state=blocked
    elif ((rc)); then state=failed; fi
    jq -n --arg cwd "${cwd}" --arg state "${state}" --argjson code "${rc}" \
       '{argv_recorded:false,cwd:$cwd,exit_code:$code,state:$state}' >"${directory}/process.json"
    PROCESS_CODE=${rc}
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
