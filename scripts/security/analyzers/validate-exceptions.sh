#!/usr/bin/env bash
# shellcheck source=../../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../../lib/common.sh"
[[ $# == 1 ]] || die 'Usage: validate-exceptions.sh REGISTRY'
invalid() { printf '{"state":"error","reason":"Invalid/expired exception metadata"}\n'; exit 2; }
[[ -f $1 ]] || invalid
registry_size=$(stat -c %s -- "$1") || invalid
if [[ ${registry_size} -gt 2097152 ]]; then invalid; fi
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
strict_json "$1" || invalid
stream_fields=()
today=$(date -u +%F)
jq -e --arg today "${today}" '
    type=="array" and all(.[];
      type=="object" and keys==["component","control","expires","finding","id","owner","reason","reviewed","tool"] and
      all(.[];type=="string" and test("\\S")) and
      (.reviewed|test("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")) and (.expires|test("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")) and
      .reviewed<=$today and .expires>$today and .expires>.reviewed) and
    ([.[]|[.tool,.finding,.component]]|length== (unique|length))' "$1" >/dev/null || invalid
# shellcheck disable=SC2016 # jq variables belong to the quoted program.
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
capture_lines stream_fields jq -r '.[]|.reviewed,.expires' "$1" || exit 2
for value in "${stream_fields[@]}"; do
    checked_date=$(date -ud "${value}" +%F) || exit 2
    [[ ${checked_date} == "${value}" ]] || invalid
done
jq '{valid:length,passed:true,applied:false}' "$1"
