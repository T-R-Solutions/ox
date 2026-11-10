#!/usr/bin/env bash
# Explicit acquisition/import only; checks never invoke this command.
# shellcheck source=../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib/common.sh"
# shellcheck source=../lib/files.sh
source "$LIB_DIR/files.sh"
review='' imports='' download=false
selected=()
while (($#)); do
    case $1 in
        --root|--review|--import|--only)
            (($# >= 2)) || die "Missing value: $1"
            case $1 in
                --root) ROOT=$2;; --review) review=$2;; --import) imports=$2;;
                --only) IFS=, read -ra selected <<<"$2";;
            esac; shift 2;;
        --download) download=true; shift;;
        --help|-h)
            printf 'Usage: prepare-datasets.sh --review REVIEW.json (--download | --import DIRECTORY) [--only rustsec] [--root ROOT]\n'
            exit 0;;
        *) die "Unknown argument: $1";;
    esac
done
ROOT=$(cd -- "$ROOT" && pwd -P)
[[ -n $review && -f $review ]] || die 'Explicit review file required'
if $download; then [[ -z $imports ]] || die 'Choose download or import'
else [[ -d $imports ]] || die 'Import directory required'; fi
(("${#selected[@]}")) || selected=(rustsec)
for name in "${selected[@]}"; do
    [[ $name == rustsec ]] || die "Dataset $name is owned by toolbox; prepare it in dev_audit, not Ox"
done
need flock
base=$(contained .local/security) || die 'Unsafe preparation path'
mkdir -p -- "$base/generations"
[[ ! -L $base/generations && ! -L $base/prepare.lock && ! -L $base/datasets.json ]] || die 'Symlinked publication path'
exec 9>"$base/prepare.lock"
flock -n 9 || die 'Another preparation is active'
stage=$(mktemp -d "$base/generations/prepared-XXXXXXXX")
# Failed generations are retained for diagnostics; no existing data are removed.
cp -- "$review" "$stage/review.json"
strict_json "$stage/review.json" || die 'Invalid review JSON'
registry=$base/datasets.json
if [[ -e $registry ]]; then
    strict_json "$registry" || die 'Invalid existing registry'
    cp -- "$registry" "$stage/registry.json"
else printf '{}\n' >"$stage/registry.json"; fi
today=$(date -u +%F)
for name in "${selected[@]}"; do
    official=https://github.com/RustSec/advisory-db.git
    scanner=cargo-audit
    need "$scanner"
    row=$(jq -ce --arg name "$name" '.[$name] | select(type=="object" and
      all(.source,.license,.revision,.dataset_date,.valid_until,.reviewer,.provenance;
          type=="string" and test("\\S")))' "$stage/review.json") || die "Incomplete review: $name"
    [[ $(jq -r .source <<<"$row") == "$official" ]] || die "Unexpected official source: $name"
    published=$(jq -r .dataset_date <<<"$row")
    expiry=$(jq -r .valid_until <<<"$row")
    for value in "$published" "$expiry"; do
        [[ $value =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ && $(date -ud "$value" +%F) == "$value" ]] || die 'Invalid dataset/review date'
    done
    [[ ! $published > $today && ! $expiry < $today && ! $expiry < $published ]] || die 'Future or expired dataset review'
    # Bound review lifetime to five days from the reviewed data date.
    (( $(date -ud "$expiry" +%s) - $(date -ud "$published" +%s) <= 432000 )) || die 'Dataset review exceeds five days'
    dest=$stage/$name
    mkdir -- "$dest"
    if $download; then
        git -c core.hooksPath=/dev/null clone --no-checkout -- "$official" "$dest"
        revision=$(jq -r .revision <<<"$row")
        [[ $revision =~ ^[0-9a-f]{40}$ ]] || die 'RustSec requires an immutable commit'
        git -C "$dest" -c core.hooksPath=/dev/null checkout --detach "$revision"
    else
        input=$imports/$name
        before=$(tree_identity "$input") || die "Invalid import tree: $name"
        [[ $before == "$(jq -r .sha256 <<<"$row")" ]] || die "Import differs from reviewed digest: $name"
        cp -a -- "$input/." "$dest/"
        [[ $(tree_identity "$dest") == "$before" ]] || die 'Import changed during copy'
    fi
    identity=$(tree_identity "$dest") || die 'Nonregular or empty dataset'
    "$scanner" --version >"$stage/$name-version.txt"
    # Probe actual scanner parsing against the project lockfile, with all fetches disabled.
    rc=0
    [[ $(git -C "$dest" remote get-url origin) == "$official" &&
       $(git -C "$dest" rev-parse HEAD) == "$(jq -r .revision <<<"$row")" &&
       $(git -C "$dest" show -s --format=%cs HEAD) == "$published" &&
       -z $(git -C "$dest" -c core.fsmonitor=false status --porcelain) ]] || die 'RustSec provenance/date mismatch'
    "$scanner" audit --no-fetch --no-yanked --db "$dest" --file "$ROOT/application/Cargo.lock" --json \
        >"$stage/$name-probe.json" 2>"$stage/$name-probe.err" || rc=$?
    if ((rc > 1)) || ! jq -e '.vulnerabilities|type=="object"' "$stage/$name-probe.json" >/dev/null; then
        die 'RustSec compatibility probe failed'
    fi
    # Some scanners update cache metadata on load; bind the verified final bytes.
    identity=$(tree_identity "$dest") || die 'Invalid final dataset'
    jq -n --argjson review "$row" --arg sha "$identity" --arg mode "$download"         --arg at "$(date -u +%FT%TZ)" --arg scanner_sha "$(hash_file "$(command -v "$scanner")")"         '{review:$review,sha256:$sha,prepared_at:$at,download:($mode=="true"),scanner_sha256:$scanner_sha,
          authenticity:"Official TLS transport for downloads; imported origin is reviewer-attested. Hashes establish integrity only."}' >"$stage/$name-provenance.json"
    jq --arg name "$name" --arg path "${dest#"$ROOT"/}" --arg sha "$identity" --argjson row "$row"         '.[$name]={path:$path,sha256:$sha,valid_until:$row.valid_until,source:$row.source,license:$row.license}'         "$stage/registry.json" >"$stage/registry.next"
    mv -- "$stage/registry.next" "$stage/registry.json"
done
# One same-filesystem rename publishes the entire selected set.
mv -T -- "$stage/registry.json" "$registry"
printf 'Published reviewed registry: %s\n' "$registry"
