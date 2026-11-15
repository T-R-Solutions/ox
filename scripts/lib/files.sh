#!/usr/bin/env bash
# shellcheck disable=SC2154 # ROOT is initialized by common.sh; AUTOMATION_JSON is supplied by registry.sh.
# File trees use NUL-delimited paths and JSON manifests, never newline lists.
tree_manifest() {
    local path=$1 item rel h
    [[ -d ${path} && ! -L ${path} ]] || return 1
    local listing invalid=false
    listing=$(mktemp) || return 1
    find "${path}" -mindepth 1 -print0 >"${listing}" || { rm -f -- "${listing}"; return 1; }
    while IFS= read -r -d '' item; do
        if [[ -L ${item} || (! -f ${item} && ! -d ${item}) ]]; then
            printf 'Nonregular/symlinked entry: %s\n' "${item}" >&2
            invalid=true; break
        fi
        [[ -f ${item} ]] || continue
        rel=${item#"${path}"/}; h=$(hash_file "${item}") || return
        jq -cn --arg path "${rel}" --arg sha "${h}" '{key:$path,value:$sha}' || return 1
    done <"${listing}"
    rm -f -- "${listing}" || return 1
    ! ${invalid}
}
tree_identity() {
    local path=$1 rows
    [[ ! -L ${path} ]] || return 1
    if [[ -f ${path} ]]; then hash_file "${path}"; return; fi
    rows=$(tree_manifest "${path}") || return
    [[ -n ${rows} ]] || return 1
    # Python's historical json.dumps(sort_keys=True) escaped non-ASCII. jq -a
    # preserves that digest format, without a trailing newline in hashed bytes.
    local canonical digest
    canonical=$(printf '%s' "${rows}" | jq -acSs 'from_entries') || return 1
    digest=$(printf '%s' "${canonical}" | sha256sum) || return 1
    printf '%s' "${digest:0:64}"
}
source_snapshot() {
    local output=$1 mode=$2 item rel name dest expected file_mode dest_sha current_sha
    mkdir -- "${output}/source" || return 1
    local listing=${output}/source-paths.nul
    catalog_load
    local value matched
    local -a prune=() roots=() patterns=()
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines stream_fields jq -r '.inputs.exclude_names[]' <<<"${AUTOMATION_JSON}" || return 1
    while IFS= read -r value; do prune+=(-name "${value}" -o); done < <(printf '%s\n' "${stream_fields[@]}")
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines stream_fields jq -r '.inputs.exclude_paths[]' <<<"${AUTOMATION_JSON}" || return 1
    while IFS= read -r value; do prune+=(-path "./${value}" -o); done < <(printf '%s\n' "${stream_fields[@]}")
    unset 'prune[${#prune[@]}-1]'
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines roots jq -r '.inputs.roots[]' <<<"${AUTOMATION_JSON}" || return 1
    # shellcheck disable=SC2016 # jq variables belong to the quoted program.
    capture_lines patterns jq -r '.inputs.root_patterns[]' <<<"${AUTOMATION_JSON}" || return 1
    (cd -- "${ROOT}" && find . -mindepth 1       \( "${prune[@]}" \) -prune -o -print0) >"${listing}" || return 1
    : >"${output}/input-rows.jsonl" || return 1
    : >"${output}/mode-rows.jsonl" || return 1
    while IFS= read -r -d '' item; do
        rel=${item#./}; name=${rel##*/}; matched=false
        for value in "${roots[@]}"; do
            if [[ ${rel} == "${value}" || ${rel} == "${value}/"* ]]; then matched=true; break; fi
        done
        if ! ${matched} && [[ ${rel} != */* ]]; then
            for value in "${patterns[@]}"; do
                # shellcheck disable=SC2053 # Intentional catalog glob, never evaluated as code.
                if [[ ${name} == ${value} ]]; then matched=true; break; fi
            done
        fi
        ${matched} || continue
        if [[ -L ${ROOT}/${rel} ]]; then printf 'Unscanned source symlink: %s\n' "${rel}" >&2; return 1; fi
        [[ -d ${ROOT}/${rel} || -f ${ROOT}/${rel} ]] || return 1
        if [[ -d ${ROOT}/${rel} ]]; then
            file_mode=$(stat -c %a -- "${ROOT}/${rel}") || return 1
            jq -cn --arg path "${rel}" --arg mode "${file_mode}" '{key:$path,value:$mode}' >>"${output}/mode-rows.jsonl" || return 1
            mkdir -p -- "${output}/source/${rel}" || return 1
            chmod --reference="${ROOT}/${rel}" -- "${output}/source/${rel}" || return 1
            continue
        fi
        case ${name} in .gitleaksignore|.semgrepignore) printf 'Source ignore requires review: %s\n' "${rel}" >&2; return 1;; *) :;; esac
        if [[ ${mode} == code && ${rel} != *.rs && ${rel} != *.py ]]; then continue; fi
        [[ -f ${ROOT}/${rel} ]] || return 1
        current_sha=$(hash_file "${ROOT}/${rel}") || return 1
        expected=${current_sha} || return
        dest=${output}/source/${rel}
        mkdir -p -- "${dest%/*}" || return 1
        cp -p -- "${ROOT}/${rel}" "${dest}" || return 1
        dest_sha=$(hash_file "${dest}") || return 1
        current_sha=$(hash_file "${ROOT}/${rel}") || return 1
        [[ ${dest_sha} == "${expected}" && ${current_sha} == "${expected}" ]] || return 1
        file_mode=$(stat -c %a -- "${ROOT}/${rel}") || return 1
        jq -cn --arg path "${rel}" --arg mode "${file_mode}" '{key:$path,value:$mode}' >>"${output}/mode-rows.jsonl" || return 1
        jq -cn --arg path "${rel}" --arg sha "${expected}" '{key:$path,value:$sha}' >>"${output}/input-rows.jsonl" || return 1
    done <"${listing}"
    jq -s 'from_entries' "${output}/mode-rows.jsonl" >"${output}/input_modes.json" || return 1
    jq -s 'from_entries' "${output}/input-rows.jsonl" >"${output}/inputs.json" || return 1
    jq -e 'length>0' "${output}/inputs.json" >/dev/null
}
input_add() {
    local output=$1 rel=$2 path
    path=$(contained "${rel}") && [[ -f ${path} ]] || return 1
    path_sha=$(hash_file "${path}") || return 1
    jq --arg path "${rel}" --arg sha "${path_sha}" '. + {($path):$sha}' "${output}/inputs.json" >"${output}/inputs.next" || return 1
    mv -- "${output}/inputs.next" "${output}/inputs.json" || return 1
}
verify_inputs() {
    local output=$1 rel expected file observed snapshot_mode mode
    if [[ -f ${output}/input_modes.json ]]; then
        jq -j 'to_entries[] | .key,"\u0000",.value,"\u0000"' "${output}/input_modes.json" >"${output}/.modes.nul" || return 1
        while IFS= read -r -d '' rel && IFS= read -r -d '' expected; do
            file=$(contained "${rel}") || return 1
            observed=$(stat -c %a -- "${file}") || return 1
            snapshot_mode=$(stat -c %a -- "${output}/source/${rel}") || return 1
            [[ ${observed} == "${expected}" && ! -L ${output}/source/${rel} && ${snapshot_mode} == "${expected}" ]] || return 1
        done <"${output}/.modes.nul"
    fi
    jq -j 'to_entries[] | .key,"\u0000",.value,"\u0000"' "${output}/inputs.json" >"${output}/.inputs.nul" || return 1
    while IFS= read -r -d '' rel && IFS= read -r -d '' expected; do
        file=$(contained "${rel}") || return 1
        [[ -f ${file} ]] || return 1
        observed=$(hash_file "${file}") || return 1
        [[ ${observed} == "${expected}" ]] || return 1
        mode=''
        if [[ -f ${output}/input_modes.json ]]; then
            mode=$(jq -r --arg rel "${rel}" '.[$rel] // empty' "${output}/input_modes.json") || return 1
            observed=$(stat -c %a -- "${file}") || return 1
            [[ -z ${mode} || ${observed} == "${mode}" ]] || return 1
        fi
        file=${output}/source/${rel}
        [[ ! -L ${file} ]] || return 1
        if [[ -f ${file} ]]; then
            observed=$(stat -c %a -- "${file}") || return 1
            [[ -z ${mode} || ${observed} == "${mode}" ]] || return 1
            observed=$(hash_file "${file}") || return 1
            [[ ${observed} == "${expected}" ]] || return 1
        fi
    done <"${output}/.inputs.nul"
}
reviewed_dataset() {
    local name=$1 output=$2 registry row relative expiry today observed
    registry=$(local_path datasets)/datasets.json && [[ -f ${registry} ]] || return 1
    strict_json "${registry}" || return
    row=$(jq -ce --arg name "${name}" '.[$name] | select(type=="object" and (keys==["license","path","sha256","source","valid_until"]) and all(.[]; type=="string" and test("\\S")))' "${registry}") || return
    relative=$(jq -r .path <<<"${row}") || return 1
    PREPARED=$(contained "${relative}") || { printf 'Dataset must stay relative to repository\n' >&2; return 1; }
    expiry=$(jq -r .valid_until <<<"${row}") || return 1
    today=$(date -u +%F) || return 1 || return 1
    checked_expiry=$(date -ud "${expiry}" +%F) || return 1
    [[ ${expiry} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ && ${checked_expiry} == "${expiry}" && ! ${expiry} < ${today} ]] || { printf 'Dataset review expired/invalid\n' >&2; return 1; }
    observed=$(tree_identity "${PREPARED}") || return
    expected_sha=$(jq -r .sha256 <<<"${row}") || return 1
    [[ ${observed} == "${expected_sha}" ]] || { printf 'Dataset digest mismatch\n' >&2; return 1; }
    registry_sha=$(hash_file "${registry}") || return 1
    jq --arg hash "${registry_sha}" '.+{registry_sha256:$hash}' <<<"${row}" >"${output}/dataset.json" || return 1
    cp -a -- "${PREPARED}" "${output}/dataset" || return 1
    copied_sha=$(tree_identity "${output}/dataset") || return 1
    [[ ${copied_sha} == "${observed}" ]]
}
