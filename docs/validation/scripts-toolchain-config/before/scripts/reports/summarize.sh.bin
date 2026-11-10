#!/usr/bin/env bash
# shellcheck source=../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib/common.sh"
[[ $# == 1 ]] || die 'Usage: summarize.sh RESULTS.json'
strict_json "$1" || die 'Invalid report'
jq -e '.product_acceptance==false and (.results|type=="array" and length>0) and
  all(.results[];.state as $state | (.argv|type=="array" and all(.[];type=="string")) and
  (.exit_code|type=="number" and floor==. and .>=0 and .<=255) and
  (["passed","recorded","findings","failed","error","blocked"]|index($state)!=null))' "$1" >/dev/null || die 'Invalid results document'
jq -r '
  def cell: tostring|gsub("\\|";"\\|")|gsub("[\\r\\n]";" ");
  "Check observations; no product approval.\n",
  "| Command | State | Exit |", "| --- | --- | --- |",
  (.results[] | "| \((.argv|join(" "))|cell) | \(.state|cell) | \(.exit_code) |"),
  (.omitted[]? | "\nOmitted: \(tojson)"), (.manual_evidence[]? | "\nManual evidence: \(.)")' "$1"
exit "$(jq -r '[.results[].exit_code|select(.!=0)][0]//0' "$1")"
