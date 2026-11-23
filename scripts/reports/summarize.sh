#!/usr/bin/env bash
# shellcheck source=../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../lib/common.sh"
[[ $# == 1 ]] || die 'Usage: summarize.sh RESULTS.json'
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
strict_json "$1" || die 'Invalid report'
jq -e '.product_acceptance==false and (.results|type=="array" and length>0) and
  all(.results[];.state as $state | (.check|type=="string" and length>0) and
  (.exit_code|type=="number" and floor==. and .>=0 and .<=255) and
  (["passed","recorded","findings","failed","error","blocked"]|index($state)!=null))' "$1" >/dev/null || die 'Invalid results document'
jq -r '
  def cell: tostring|gsub("\\|";"\\|")|gsub("[\\r\\n]";" ");
  "Check observations; no product approval.\n",
  "| Check | State | Exit |", "| --- | --- | --- |",
  (.results[] | "| \((.check)|cell) | \(.state|cell) | \(.exit_code) |"),
  (.omitted[]? | "\nOmitted: \(tojson)"), (.manual_evidence[]? | "\nManual evidence: \(.)")' "$1"
# shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
aggregate_code=$(aggregate_results "$1") || exit 2
exit "${aggregate_code}"
