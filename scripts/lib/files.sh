#!/usr/bin/env bash
# File trees use NUL-delimited paths and JSON manifests, never newline lists.
tree_manifest() {
    local path=$1 item rel h
    [[ -d $path && ! -L $path ]] || return 1
    local listing invalid=false
    listing=$(mktemp)
    find "$path" -mindepth 1 -print0 >"$listing" || { rm -f -- "$listing"; return 1; }
    while IFS= read -r -d '' item; do
        if [[ -L $item || (! -f $item && ! -d $item) ]]; then
            printf 'Nonregular/symlinked entry: %s\n' "$item" >&2
            invalid=true; break
        fi
        [[ -f $item ]] || continue
        rel=${item#"$path"/}; h=$(hash_file "$item") || return
        jq -cn --arg path "$rel" --arg sha "$h" '{key:$path,value:$sha}'
    done <"$listing"
    rm -f -- "$listing"
    ! $invalid
}
tree_identity() {
    local path=$1 rows
    [[ ! -L $path ]] || return 1
    if [[ -f $path ]]; then hash_file "$path"; return; fi
    rows=$(tree_manifest "$path") || return
    [[ -n $rows ]] || return 1
    # Python's historical json.dumps(sort_keys=True) escaped non-ASCII. jq -a
    # preserves that digest format, without a trailing newline in hashed bytes.
    printf '%s' "$rows" | jq -acSs 'from_entries' | tr -d '\n' | sha256sum | cut -c 1-64
}
source_snapshot() {
    local output=$1 mode=$2 item rel name dest expected
    mkdir -- "$output/source"
    local listing=$output/source-paths.nul
    (cd -- "$ROOT" && find . -mindepth 1 \
      \( -name .git -o -name .local -o -name target -o -name dist -o -name __pycache__ -o -name .venv -o -name venv -o -path ./docs/validation \) -prune -o -print0) >"$listing"
    : >"$output/input-rows.jsonl"
    : >"$output/mode-rows.jsonl"
    while IFS= read -r -d '' item; do
        rel=${item#./}; name=${rel##*/}
        case $rel in
            */*) case ${rel%%/*} in application|tools|scripts|sdd|config|docs|.github|.codex) :;; *) continue;; esac;;
            *) case $rel in application|tools|scripts|sdd|config|docs|.github|.codex)
                   [[ ! -L $ROOT/$rel ]] || { printf 'Unscanned source symlink: %s\n' "$rel" >&2; return 1; };; esac
               if [[ -d $ROOT/$rel ]]; then continue; fi
               case $name in *.md|*.toml|*.json|*.yml|*.yaml|*.py|*.sh|*.txt|*.lock|.env*|LICENSE|NOTICE|.gitleaksignore|.semgrepignore) :;; *) continue;; esac;;
        esac
        if [[ -L $ROOT/$rel ]]; then printf 'Unscanned source symlink: %s\n' "$rel" >&2; return 1; fi
        [[ -d $ROOT/$rel || -f $ROOT/$rel ]] || return 1
        if [[ -d $ROOT/$rel ]]; then
            jq -cn --arg path "$rel" --arg mode "$(stat -c %a -- "$ROOT/$rel")" '{key:$path,value:$mode}' >>"$output/mode-rows.jsonl"
            mkdir -p -- "$output/source/$rel"
            chmod --reference="$ROOT/$rel" -- "$output/source/$rel"
            continue
        fi
        case $name in .gitleaksignore|.semgrepignore) printf 'Source ignore requires review: %s\n' "$rel" >&2; return 1;; esac
        if [[ $mode == code && $rel != *.rs && $rel != *.py ]]; then continue; fi
        [[ -f $ROOT/$rel ]] || return 1
        expected=$(hash_file "$ROOT/$rel") || return
        dest=$output/source/$rel
        mkdir -p -- "${dest%/*}"
        cp -p -- "$ROOT/$rel" "$dest"
        [[ $(hash_file "$dest") == "$expected" && $(hash_file "$ROOT/$rel") == "$expected" ]] || return 1
        jq -cn --arg path "$rel" --arg mode "$(stat -c %a -- "$ROOT/$rel")" '{key:$path,value:$mode}' >>"$output/mode-rows.jsonl"
        jq -cn --arg path "$rel" --arg sha "$expected" '{key:$path,value:$sha}' >>"$output/input-rows.jsonl"
    done <"$listing"
    jq -s 'from_entries' "$output/mode-rows.jsonl" >"$output/input_modes.json"
    jq -s 'from_entries' "$output/input-rows.jsonl" >"$output/inputs.json"
    jq -e 'length>0' "$output/inputs.json" >/dev/null
}
input_add() {
    local output=$1 rel=$2 path
    path=$(contained "$rel") && [[ -f $path ]] || return 1
    jq --arg path "$rel" --arg sha "$(hash_file "$path")" '. + {($path):$sha}' "$output/inputs.json" >"$output/inputs.next"
    mv -- "$output/inputs.next" "$output/inputs.json"
}
verify_inputs() {
    local output=$1 rel expected file
    if [[ -f $output/input_modes.json ]]; then
        while IFS= read -r -d '' rel && IFS= read -r -d '' expected; do
            file=$(contained "$rel") || return 1
            [[ $(stat -c %a -- "$file") == "$expected" && ! -L $output/source/$rel &&
                $(stat -c %a -- "$output/source/$rel") == "$expected" ]] || return 1
        done < <(jq -j 'to_entries[] | .key,"\u0000",.value,"\u0000"' "$output/input_modes.json")
    fi
    while IFS= read -r -d '' rel && IFS= read -r -d '' expected; do
        file=$(contained "$rel") && [[ -f $file && $(hash_file "$file") == "$expected" ]] || return 1
        if [[ -f $output/input_modes.json ]]; then
            local mode
            mode=$(jq -r --arg rel "$rel" '.[$rel] // empty' "$output/input_modes.json")
            [[ -z $mode || $(stat -c %a -- "$file") == "$mode" ]] || return 1
        fi
        file=$output/source/$rel
        [[ ! -L $file ]] || return 1
        [[ ! -f $file || -z ${mode:-} || $(stat -c %a -- "$file") == "$mode" ]] || return 1
        [[ ! -f $file || $(hash_file "$file") == "$expected" ]] || return 1
    done < <(jq -j 'to_entries[] | .key,"\u0000",.value,"\u0000"' "$output/inputs.json")
}
reviewed_dataset() {
    local name=$1 output=$2 registry row relative expiry today observed
    registry=$(contained .local/security/datasets.json) && [[ -f $registry ]] || return 1
    strict_json "$registry" || return
    row=$(jq -ce --arg name "$name" '.[$name] | select(type=="object" and (keys==["license","path","sha256","source","valid_until"]) and all(.[]; type=="string" and test("\\S")))' "$registry") || return
    relative=$(jq -r .path <<<"$row")
    PREPARED=$(contained "$relative") || { printf 'Dataset must stay relative to repository\n' >&2; return 1; }
    expiry=$(jq -r .valid_until <<<"$row"); today=$(date -u +%F)
    [[ $expiry =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ && $(date -ud "$expiry" +%F) == "$expiry" && ! $expiry < $today ]] || { printf 'Dataset review expired/invalid\n' >&2; return 1; }
    observed=$(tree_identity "$PREPARED") || return
    [[ $observed == "$(jq -r .sha256 <<<"$row")" ]] || { printf 'Dataset digest mismatch\n' >&2; return 1; }
    jq --arg hash "$(hash_file "$registry")" '.+{registry_sha256:$hash}' <<<"$row" >"$output/dataset.json"
    cp -a -- "$PREPARED" "$output/dataset"
    [[ $(tree_identity "$output/dataset") == "$observed" ]]
}
