#!/usr/bin/env bash
# shellcheck source=../../lib/common.sh
source "$(dirname -- "${BASH_SOURCE[0]}")/../../lib/common.sh"
# shellcheck source=../../lib/reports.sh
source "${LIB_DIR}/reports.sh"
[[ $# == 3 && $1 == --parser ]] || die 'Usage: check-report.sh --parser NAME REPORT'
# shellcheck disable=SC2310 # Status predicate: failures are propagated explicitly by the called function.
if [[ -f $3 ]] && report_size=$(stat -c %s -- "$3") &&
   [[ ${report_size} -le 8388608 ]] && count=$(finding_count "$2" "$3"); then
    state=passed; ((count==0)) || state=findings
    jq -n --arg state "${state}" --argjson count "${count}" '{state:$state,count:$count}'
    ((count==0))
else
    printf '{"state":"error","reason":"Invalid or incomplete report"}\n'
    exit 2
fi
