#!/usr/bin/env bash
# Two-date retention; caller owns temporary work and propagates publication errors.
retain_logs() (
    set -Eeuo pipefail
    local root=$1 run=${2:-} apply=${3:-true} day=${4:-} base path name rel dest
    if [[ -z ${day} ]]; then day=$(date +%F) || return 2; fi
    [[ -d ${root} && ! -L ${root}/.local ]] || return 2
    mkdir -p -- "${root}/.local" || return 2
    base=${root}/.local/logs
    [[ ! -L ${base} ]] || return 2
    mkdir -p -- "${base}" || return 2
    # Lock the directory inode; no persistent auxiliary lock or backup receipt.
    exec 9<"${base}" || return 2
    flock -x 9 || return 2
    local -a dates=()
    shopt -s nullglob dotglob
    for path in "${base}"/*; do
        name=${path##*/}
        checked_day=$(date -d "${name}" +%F) || return 1
        [[ -d ${path} && ! -L ${path} && ${name} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ && ${checked_day} == "${name}" ]] || return 2
        dates+=("${name}")
    done
    if [[ -n ${run} ]]; then
        owner=$(cat "${run}/.owner") || return 1
        [[ ! -L ${run} && -f ${run}/.owner && ${owner} == ox-local-v2 ]] || return 2
        checked_day=$(date -d "${day}" +%F) || return 1
        [[ ${day} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ && ${checked_day} == "${day}" ]] || return 2
        local date_rows
        date_rows=$(printf '%s\n' "${dates[@]}" "${day}" | LC_ALL=C sort -u) || return 2
        mapfile -t dates <<<"${date_rows}" || return 2
        ((${#dates[@]}<3)) || [[ ${day} > ${dates[-3]} ]] || return 2
    fi
    local i
    for ((i=0; i<${#dates[@]}-2; i++)); do
        path=${base}/${dates[i]}
        printf 'Removing oldest date: %s (apply=%s)\n' "${path}" "${apply}"
        if [[ ${apply} == true ]]; then rm -rf -- "${path}" || return 2; fi
    done
    [[ -n ${run} ]] || return 0
    mkdir -p -- "${base}/${day}" || return 2
    find "${run}" \( -type d \( -name source -o -name dataset -o -name target -o -name cache -o -name home -o -name .git \) -prune \) -o \
        -type f \( -name '*.log' -o -name '*.json' -o -name '*.jsonl' -o -name '*.err' -o -name '*.txt' \) -print0 >"${run}/.log-paths" || return 2
    while IFS= read -r -d '' path; do
        rel=${path#"${run}"/}
        rel=${rel//%/%25}; rel=${rel//-/%2D}; rel=${rel//\//--}
        dest=${base}/${day}/${run##*/}--${rel}.log
        # noclobber refuses existing files and symlinks without overwriting logs.
        (set -o noclobber; cat -- "${path}" >"${dest}") || return 2
    done <"${run}/.log-paths"
    rm -rf -- "${run}" || return 2
    printf 'Logs: %s/%s\n' "${base}" "${day}"
)
