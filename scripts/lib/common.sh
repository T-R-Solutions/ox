#!/usr/bin/env bash
# Shared startup, JSON and path primitives. Source from an entry, never execute.
set -Eeuo pipefail
umask 077
LIB_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
SCRIPTS_DIR=$(dirname -- "${LIB_DIR}")
ROOT=$(dirname -- "${SCRIPTS_DIR}")
export PYTHONDONTWRITEBYTECODE=1 CARGO_NET_OFFLINE=true RUSTUP_AUTO_INSTALL=0

die() { printf '%s\n' "$*" >&2; exit 2; }
need() { command -v "$1" >/dev/null || die "Required command missing: $1"; }
need jq
hash_file() { local h; h=$(sha256sum <"$1") || return; printf '%s' "${h:0:64}"; }
json_args() { if (($#)); then printf '%s\0' "$@" | jq -Rs 'split("\u0000")[:-1]'; else printf '[]\n'; fi; }

# jq normally accepts duplicate object keys. Streaming events retain them. Track
# each node as its parent is entered, including empty containers and close events.
strict_json() {
    [[ -f $1 && -r $1 ]] || return 1
    # Validate tokens without repeatedly copying an entire unquoted line.
    # jq accepts nonfinite literals; allow only JSON keywords and exponent letters.
    LC_ALL=C awk 'function word_end() {
      if (word!="" && word!="true" && word!="false" && word!="null" && word!="e" && word!="E") exit 1
      word=""
    }
    BEGIN {q=0; esc=0; word=""}
    {
      for(i=1;i<=length($0);i++) {
        c=substr($0,i,1)
        if(q) {
          if(esc) esc=0
          else if(c=="\\") esc=1
          else if(c=="\"") q=0
        } else if(c ~ /[a-zA-Z]/) {
          word=word c
          if(length(word)>5) exit 1
        } else {
          word_end()
          if(c=="\"") q=1
          else if(c !~ /[0-9[:space:]{}[\],: .+\-]/) exit 1
        }
      }
      word_end()
    }
    END {if(q) exit 1}' "$1" || return
    jq --stream -n '
      reduce inputs as $e ({seen:{}, active:[], roots:0};
        if ($e|length)==1 then .active=$e[0][:-2]
        else $e[0] as $p |
          if ($p|length)==0 then .roots+=1 else . end |
          reduce range(1; ($p|length)+1) as $i (.;
            ($p[:$i]|tojson) as $key |
            if .active[:$i] == $p[:$i] then .
            elif .seen[$key] then error("duplicate JSON key")
            else .seen[$key]=true end) |
          .active=$p[:-1]
        end) | true' "$1" >/dev/null || return
    # Exactly one document; reject nonfinite numbers (jq normalizes NaN to null).
    jq -es 'length==1' "$1" >/dev/null
}
contained() {
    local rel=$1 part current=${ROOT}
    [[ ${rel} != /* && ${rel} != *$'\n'* ]] || return 1
    local -a parts
    IFS=/ read -ra parts <<< "${rel}"
    for part in "${parts[@]}"; do
        [[ ${part} != .. ]] || return 1
        current+=/${part}
        [[ ! -L ${current} ]] || return 1
    done
    printf '%s\n' "${current}"
}
local_path() {
    # shellcheck source=registry.sh
    source "${LIB_DIR}/registry.sh" || return 1
    catalog_load
    local relative
    relative=$(jq -er --arg key "$1" '.paths[$key] // error("Unknown local category")' <<<"${AUTOMATION_JSON}") || die 'Unknown local category'
    contained "${relative}"
}
run_lease() {
    local run=$1 owner
    owner=$(cat "${run}/.owner") || return 1
    [[ -f ${run}/.owner && ${owner} == ox-local-v2 ]] || die 'Unowned run'
    export OX_ACTIVE_RUN=${run}
}
run_complete() {
    local completed_run=$1 rc=0 owner
    owner=$(cat "${completed_run}/.owner") || return 1
    [[ ! -L ${completed_run} && -f ${completed_run}/.owner && ${owner} == ox-local-v2 ]] || return 2
    # shellcheck source=logs.sh
    source "${LIB_DIR}/logs.sh" || return 2
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    retain_logs "${ROOT}" "${completed_run}" || rc=$?
    # Even a publication failure must not retain source or dataset copies.
    rm -rf -- "${completed_run}" || return 2
    return "${rc}"
}
new_run() {
    local run
    run=$(mktemp -d "${TMPDIR:-/tmp}/ox-$1-XXXXXXXX") || return
    printf 'ox-local-v2\n' >"${run}/.owner" || return 1
    printf '%s\n' "${run}"
}

# A failed producer must not become an empty, successful mapfile.
capture_lines() {
    local destination=$1 captured
    shift
    captured=$("$@") || return
    local -n captured_array=${destination}
    captured_array=()
    # shellcheck disable=SC2034 # Nameref writes the caller-owned destination array.
    if [[ -n ${captured} ]]; then mapfile -t captured_array <<<"${captured}"; fi
}

# Preserve NUL-delimited producer status separately from array loading.
capture_nul() {
    local destination=$1 temporary rc=0
    shift
    temporary=$(mktemp) || return 1
    if "$@" >"${temporary}"; then
        local -n nul_array=${destination}
        # shellcheck disable=SC2034 # Nameref writes the caller-owned destination array.
        mapfile -d '' -t nul_array <"${temporary}" || rc=$?
    else rc=$?; fi
    rm -f -- "${temporary}" || return 1
    return "${rc}"
}
