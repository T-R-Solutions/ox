#!/usr/bin/env bash
# shellcheck disable=SC2034 # STATE/CODE/COUNT are returned to shell callers.
# Strict scanner schemas shared by the runner and standalone analyzer.
finding_count() {
    local parser=$1 report=$2
    [[ -f ${report} && ! -L ${report} ]] || return 1
    strict_json "${report}" || return
    jq -er --arg p "${parser}" '
      def arr: type=="array";
      def obj: type=="object";
      def require($ok): if $ok then . else error("invalid/incomplete report: "+$p) end;
      if ["gitleaks","history","shellcheck","pssa"]|index($p) then
        require(arr and all(.[];obj)) | length
      elif $p=="opengrep" then
        require(obj and (.results|arr) and (.errors|arr and length==0) and
          (.paths.scanned|arr and length>0) and ((.paths.skipped//[])|arr and length==0) and
          all(.results[];obj and (.check_id|type=="string") and ((.extra.is_ignored//false)==false))) | .results|length
      elif $p=="osv" then
        require(obj and (.results|arr) and ((.errors//[])|length==0) and all(.results[];(.packages|arr))) |
        [.results[].packages[]] | require(length>0 and all(.[];obj and (.package|obj) and ((.vulnerabilities//[])|arr))) |
        [.[].vulnerabilities//[]|length]|add//0
      elif $p=="sarif" then
        require(obj and (.runs|arr and length>0) and all(.runs[];obj and (.tool|obj) and
          (.results|arr) and (.invocations|arr and length>0) and all(.invocations[];.executionSuccessful==true))) |
        [.runs[].results|length]|add
      elif $p=="json-findings" then require(.complete==true and (.findings|arr))|.findings|length
      elif $p=="syft" or $p=="sbom" then require((.artifacts|arr and length>0) and (.descriptor|obj))|0
      elif $p=="grype" then require((.matches|arr) and (.descriptor|obj) and (.source|obj))|.matches|length
      elif $p=="yara" or $p=="malware" then
        require((.version|type=="string") and (.matches|arr) and all(.matches[];obj and (.rule|type=="string") and (.file|type=="string")))|.matches|length
      elif $p=="audit" then
        require((.vulnerabilities.list|arr) and (.vulnerabilities.count==(.vulnerabilities.list|length)) and
          (.database|obj) and (.lockfile|obj) and ((.warnings//{})|obj and all(.[];arr))) |
        (.vulnerabilities.list|length) + ([(.warnings//{})[]|length]|add//0)
      elif $p=="trivy" then
        require(.SchemaVersion==2 and (.Results|arr and length>0) and all(.Results[];
          obj and ((.Vulnerabilities//[])|arr) and ((.Misconfigurations//[])|arr) and
          ((.Secrets//[])|arr) and ((.ExperimentalModifiedFindings//[])|arr and length==0) and
          all((.Misconfigurations//[])[]; .Status=="FAIL" or .Status=="PASS" or .Status=="EXCEPTION"))) |
        [.Results[]| ((.Vulnerabilities//[])|length) + ((.Secrets//[])|length) +
          ([(.Misconfigurations//[])[]|select(.Status!="PASS")]|length)]|add
      elif $p=="bandit" then require((.errors|arr and length==0) and (.metrics|obj and length>0) and (.results|arr))|.results|length
      elif $p=="ruff" then require(arr and all(.[];obj and has("code")))|length
      elif $p=="machete" then require(obj and (.crates|arr) and all(.crates[];(.unused|arr)))|[.crates[].unused|length]|add//0
      elif $p=="geiger" then require((.packages|arr and length>0) and (.packages_without_metrics|arr and length==0) and (.used_but_not_scanned_files|arr and length==0))|0
      else error("unsupported parser: "+$p) end' "${report}"
}

# Redact before exporting a native Trivy report. On malformed output, retain
# identity/size and a diagnostic, never unparsed secret-bearing bytes.
redact_trivy() {
    local report=$1 output=$2 temporary
    temporary=${output}/.redacted-trivy
    [[ -f ${report} && ! -L ${report} ]] || return 1
    report_sha=$(hash_file "${report}") || return 1
    report_bytes=$(wc -c <"${report}") || return 1
    jq -n --arg sha "${report_sha}" --argjson bytes "${report_bytes}" \
        '{raw_sha256:$sha,raw_bytes:$bytes,projection:"Trivy secret values/code removed",raw_retained:false}' >"${output}/redaction.json"
    if strict_json "${report}" && jq -e '
      del(.Metadata.ImageConfig, .Metadata.Layers) |
      if (.Results|type)!="array" then error("Invalid Trivy Results") else
        .Results |= map(
          if ((.ExperimentalModifiedFindings//[])|length)>0 then error("Suppressed Trivy findings") else . end |
          if .Secrets then .Secrets |= map({RuleID,Category,Severity,Title,StartLine,EndLine}) else . end |
          if .Licenses then .Licenses |= map(del(.Text)) else . end |
          if .Misconfigurations then .Misconfigurations |= map(del(.CauseMetadata.Code)) else . end)
      end' "${report}" >"${temporary}" 2>/dev/null; then
        mv -- "${temporary}" "${report}"
    else
        printf '{}\n' >"${report}"
        rm -f -- "${temporary}"
        return 1
    fi
}
assess() {
    local name=$1 raw=$2 report=$3 expected=1
    STATE=passed CODE=${raw} COUNT=null
    if ((raw==126 || raw==127)); then STATE=blocked; return; fi
    if [[ ${name} == machete-text ]]; then
        local stderr=${report%/*}/stderr.log
        [[ -s ${report} && -s ${stderr} ]] || return 1
        # Version 0.9.2: errors may be printed even when the process returns zero.
        first_line=$(head -n 1 "${stderr}") || return 1
        last_line=$(tail -n 1 "${stderr}") || return 1
        [[ ${first_line} == 'Analyzing dependencies of crates in ....' &&
           ${last_line} == 'Done!' ]] || return 1
        line_count=$(wc -l <"${stderr}") || return 1
        [[ ${line_count} == 2 ]] || return 1
        if ((raw==0)); then
            report_text=$(cat "${report}") || return 1
            [[ ${report_text} == "cargo-machete didn't find any unused dependencies in this directory. Good job!" ]] || return 1
            COUNT=0
        elif ((raw==1)); then
            report_header=$(head -n 1 "${report}") || return 1
            [[ ${report_header} == 'cargo-machete found the following unused dependencies in this directory:' ]] || return 1
            grep -Fq 'ignored = ["prost"]' "${report}" || return 1
            COUNT=$(grep -c $'^\t' "${report}") || return 1
            ((COUNT>0)) || return 1
            STATE=findings
        else STATE=error; fi
        return
    fi
    if [[ ${name} == deny ]]; then
        strict_json "${report}" || return 1
        COUNT=$(jq -er '
          def nat: type=="number" and .>=0 and floor==.;
          if type=="array" and length>0 and .[-1].type=="summary" and
            ([.[]|select(.type=="summary")]|length)==1 and
            all(.[]; .type=="diagnostic" or .type=="summary") and
            (.[-1].fields|keys|sort)==["bans","licenses","sources"] and
            all(.[-1].fields[]; all(.[];nat)) and
            (.[-1].fields|[.[]|.errors]|add)==([.[:-1][]|select(.fields.severity=="error")]|length) and
            (.[-1].fields|[.[]|.warnings]|add)==([.[:-1][]|select(.fields.severity=="warning")]|length) and
            all(.[:-1][]; (.fields.code|type=="string") and
              (.fields.severity|IN("error","warning","note","help","bug")))
          then [.[:-1][]|select(.fields.severity=="error" or .fields.severity=="warning")]|length
          else error("incomplete deny stream") end' "${report}") || { COUNT=null; return 1; }
        expected=$(jq -er '.[-1].fields | (if .bans.errors>0 then 2 else 0 end) + (if .licenses.errors>0 then 4 else 0 end) + (if .sources.errors>0 then 8 else 0 end)' "${report}") || return 1
        ((raw==expected)) || return 1
        if jq -e 'any(.[:-1][]; .fields.severity=="bug")' "${report}" >/dev/null; then
            STATE=error; CODE=2
        elif ((COUNT==0)); then STATE=passed CODE=0
        elif ((COUNT>0)); then STATE=findings; ((CODE)) || CODE=1
        else return 1; fi
        return
    fi
    if [[ ${name} == coverage ]]; then
        if ((raw)); then STATE=failed; return; fi
        [[ -f ${report} ]] && grep -Eq $'^end_of_record\r?$' "${report}" || return 1
        STATE=recorded
        return
    fi
    COUNT=$(finding_count "${name}" "${report}") || { COUNT=null; return 1; }
    [[ ${name} != gitleaks && ${name} != history ]] || expected=10
    if ((raw!=0 && raw!=expected)) || ((raw && COUNT==0)); then STATE=failed
    elif ((COUNT)); then STATE=findings; ((CODE)) || CODE=1
    elif [[ ${name} == geiger || ${name} == sbom ]]; then STATE=recorded
    fi
}
