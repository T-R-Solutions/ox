#!/usr/bin/env bash
# Explicit acquisition/import only; checks never invoke this command.
# shellcheck source=../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib/common.sh"
# shellcheck source=../lib/files.sh
source "${LIB_DIR}/files.sh"
review='' imports='' download=false
selected=()
while (($#)); do
    case $1 in
        --root|--review|--import|--only)
            (($# >= 2)) || die "Missing value: $1"
            case $1 in
                --root) ROOT=$2;; --review) review=$2;; --import) imports=$2;;
                --only) IFS=, read -ra selected <<<"$2";;
                *) :;; # Other validated classifications require no action.
            esac; shift 2;;
        --download) download=true; shift;;
        --help|-h)
            printf 'Usage: prepare-datasets.sh --review REVIEW.json (--download | --import DIRECTORY) [--only rustsec] [--root ROOT]\n'
            exit 0;;
        *) die "Unknown argument: $1";;
    esac
done
ROOT=$(cd -- "${ROOT}" && pwd -P)
[[ -n ${review} && -f ${review} ]] || die 'Explicit review file required'
if ${download}; then [[ -z ${imports} ]] || die 'Choose download or import'
else [[ -d ${imports} ]] || die 'Import directory required'; fi
(("${#selected[@]}")) || selected=(rustsec)
for name in "${selected[@]}"; do
    [[ ${name} == rustsec ]] || die "Dataset ${name} is owned by toolbox; prepare it in dev_audit, not Ox"
done
need flock
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
base=$(local_path datasets) || die 'Unsafe preparation path'
mkdir -p -- "${base}/generations"
[[ ! -L ${base}/generations && ! -L ${base}/prepare.lock && ! -L ${base}/datasets.json ]] || die 'Symlinked publication path'
exec 9>"${base}/prepare.lock"
flock -n 9 || die 'Another preparation is active'
stage=$(mktemp -d "${base}/generations/prepared-XXXXXXXX")
# Failed staging is disposable; keep only the published generation.
trap 'rc=$?; if ((rc)); then rm -rf -- "$stage"; fi' EXIT
cp -- "${review}" "${stage}/review.json"
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
strict_json "${stage}/review.json" || die 'Invalid review JSON'
registry=${base}/datasets.json
if [[ -e ${registry} ]]; then
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    strict_json "${registry}" || die 'Invalid existing registry'
    cp -- "${registry}" "${stage}/registry.json"
else printf '{}\n' >"${stage}/registry.json"; fi
today=$(date -u +%F)
for name in "${selected[@]}"; do
    official=https://github.com/RustSec/advisory-db.git
    scanner=cargo-audit
    need "${scanner}"
    row=$(jq -ce --arg name "${name}" '.[$name] | select(type=="object" and
      all(.source,.license,.revision,.dataset_date,.valid_until,.reviewer,.provenance;
          type=="string" and test("\\S")))' "${stage}/review.json") || die "Incomplete review: ${name}"
    review_source=$(jq -r .source <<<"${row}") || exit 2
    [[ ${review_source} == "${official}" ]] || die "Unexpected official source: ${name}"
    published=$(jq -r .dataset_date <<<"${row}")
    expiry=$(jq -r .valid_until <<<"${row}")
    for value in "${published}" "${expiry}"; do
        checked_date=$(date -ud "${value}" +%F) || exit 2
        [[ ${value} =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ && ${checked_date} == "${value}" ]] || die 'Invalid dataset/review date'
    done
    [[ ! ${published} > ${today} && ! ${expiry} < ${today} && ! ${expiry} < ${published} ]] || die 'Future or expired dataset review'
    # Bound review lifetime to five days from the reviewed data date.
    expiry_seconds=$(date -ud "${expiry}" +%s) || exit 2
    published_seconds=$(date -ud "${published}" +%s) || exit 2
    (( expiry_seconds - published_seconds <= 432000 )) || die 'Dataset review exceeds five days'
    dest=${stage}/${name}
    mkdir -- "${dest}"
    if ${download}; then
        git -c core.hooksPath=/dev/null clone --no-checkout -- "${official}" "${dest}"
        review_revision=$(jq -r .revision <<<"${row}") || exit 2
        revision=${review_revision}
        [[ ${revision} =~ ^[0-9a-f]{40}$ ]] || die 'RustSec requires an immutable commit'
        git -C "${dest}" -c core.hooksPath=/dev/null checkout --detach "${revision}"
    else
        input=${imports}/${name}
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        before=$(tree_identity "${input}") || die "Invalid import tree: ${name}"
        expected_sha=$(jq -r .sha256 <<<"${row}") || exit 2
        [[ ${before} == "${expected_sha}" ]] || die "Import differs from reviewed digest: ${name}"
        cp -a -- "${input}/." "${dest}/"
        # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
        copied_sha=$(tree_identity "${dest}") || exit 2
        [[ ${copied_sha} == "${before}" ]] || die 'Import changed during copy'
    fi
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    copied_sha=$(tree_identity "${dest}") || exit 2
    identity=${copied_sha} || die 'Nonregular or empty dataset'
    "${scanner}" --version >"${stage}/${name}-version.txt"
    # Probe actual scanner parsing against the project lockfile, with all fetches disabled.
    rc=0
    origin=$(git -C "${dest}" remote get-url origin) || exit 2
    head=$(git -C "${dest}" rev-parse HEAD) || exit 2
    review_revision=$(jq -r .revision <<<"${row}") || exit 2
    head_date=$(git -C "${dest}" show -s --format=%cs HEAD) || exit 2
    git_status=$(git -C "${dest}" -c core.fsmonitor=false status --porcelain) || exit 2
    [[ ${origin} == "${official}" &&
       ${head} == "${review_revision}" &&
       ${head_date} == "${published}" &&
       -z ${git_status} ]] || die 'RustSec provenance/date mismatch'
    "${scanner}" audit --no-fetch --no-yanked --db "${dest}" --file "${ROOT}/application/Cargo.lock" --json \
        >"${stage}/${name}-probe.json" 2>"${stage}/${name}-probe.err" || rc=$?
    if ((rc > 1)) || ! jq -e '.vulnerabilities|type=="object"' "${stage}/${name}-probe.json" >/dev/null; then
        die 'RustSec compatibility probe failed'
    fi
    # Some scanners update cache metadata on load; bind the verified final bytes.
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    copied_sha=$(tree_identity "${dest}") || exit 2
    identity=${copied_sha} || die 'Invalid final dataset'
    prepared_at=$(date -u +%FT%TZ) || exit 2
    scanner_path=$(command -v "${scanner}") || exit 2
    # shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
    scanner_sha=$(hash_file "${scanner_path}") || exit 2
    jq -n --argjson review "${row}" --arg sha "${identity}" --arg mode "${download}"         --arg at "${prepared_at}" --arg scanner_sha "${scanner_sha}"         '{review:$review,sha256:$sha,prepared_at:$at,download:($mode=="true"),scanner_sha256:$scanner_sha,
          authenticity:"Official TLS transport for downloads; imported origin is reviewer-attested. Hashes establish integrity only."}' >"${stage}/${name}-provenance.json"
    jq --arg name "${name}" --arg path "${dest#"${ROOT}"/}" --arg sha "${identity}" --argjson row "${row}"         '.[$name]={path:$path,sha256:$sha,valid_until:$row.valid_until,source:$row.source,license:$row.license}'         "${stage}/registry.json" >"${stage}/registry.next"
    mv -- "${stage}/registry.next" "${stage}/registry.json"
done
# One same-filesystem rename publishes the entire selected set.
mv -T -- "${stage}/registry.json" "${registry}"
for old in "${base}"/generations/prepared-*; do
    [[ ${old} == "${stage}" || ! -d ${old} || -L ${old} ]] || rm -rf -- "${old}"
done
printf 'Published reviewed registry: %s\n' "${registry}"
