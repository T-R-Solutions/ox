#!/usr/bin/env bash
# shellcheck source=../../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../../lib/common.sh"
[[ $# == 1 ]] || die 'Usage: validate-exceptions.sh REGISTRY'
invalid() { printf '{"state":"error","reason":"Invalid/expired exception metadata"}\n'; exit 2; }
if [[ ! -f $1 || $(stat -c %s -- "$1") -gt 2097152 ]]; then invalid; fi
strict_json "$1" || invalid
today=$(date -u +%F)
jq -e --arg today "$today" '
    type=="array" and all(.[];
      type=="object" and keys==["component","control","expires","finding","id","owner","reason","reviewed","tool"] and
      all(.[];type=="string" and test("\\S")) and
      (.reviewed|test("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")) and (.expires|test("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")) and
      .reviewed<=$today and .expires>$today and .expires>.reviewed) and
    ([.[]|[.tool,.finding,.component]]|length== (unique|length))' "$1" >/dev/null || invalid
while IFS= read -r value; do
    [[ $(date -ud "$value" +%F) == "$value" ]] || invalid
done < <(jq -r '.[]|.reviewed,.expires' "$1")
jq '{valid:length,passed:true,applied:false}' "$1"
