#!/usr/bin/env bash
# Human projection only. Raw streams and assessment/result JSON remain authorities.
# shellcheck disable=SC2034,SC2154 # State is shared with automate.sh/process.sh.
# Retained-log names have one encoder, shared with the publisher.
# shellcheck source=logs.sh
source "${LIB_DIR}/logs.sh"
# Fixed presentation tokens only; tool text never supplies an ANSI sequence.
progress_label() {
    local color='' label=$1
    case ${label} in SUCESSO) color=32;; FALHA) color=31;; WARNING|BLOQUEADA|IGNORADA|CANCELADA) color=33;; *) :;; esac
    if ${PROGRESS_COLOR:-false} && [[ -n ${color} ]]; then
        printf '\033[%sm%s\033[0m' "${color}" "${label}"
    else printf '%s' "${label}"; fi
}
progress_heading() {
    if ${PROGRESS_COLOR:-false}; then printf '\033[1m%s\033[0m' "$1" >&2
    else printf '%s' "$1" >&2; fi
}
progress_field() {
    local label=$1 padding
    padding=$((17-${#label})); ((padding>=0)) || padding=0
    printf '    ' >&2
    progress_label "${label}" >&2
    printf '%*s %s\n' "${padding}" '' "$2" >&2
}
progress_phase_result() {
    local label
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    label=$(progress_label "$3") || return 2
    printf '\n' >&2
    progress_heading "[${PROGRESS_INDEX}/${PROGRESS_TOTAL}] $1 (${PROGRESS_ID})"
    printf '  [%s]  | duração: %s\n' "${label}" "$2" >&2
}
progress_name() {
    case $1 in
        preparation) printf 'Preparação';; finalization) printf 'Finalização e publicação dos logs';;
        sdd-structure) printf 'Estrutura SDD';; ox) printf 'Governança Ox';;
        governance-tests) printf 'Testes de governança';; scripts-syntax) printf 'Sintaxe dos scripts';;
        scripts-tests) printf 'Testes dos scripts';; rust-fmt) printf 'Formatação Rust';;
        rust-check) printf 'Verificação Rust';; rust-build) printf 'Compilação Rust';;
        rust-test) printf 'Testes Rust';; rust-clippy) printf 'Clippy';;
        geiger) printf 'Geiger';; coverage) printf 'Cobertura';; sbom) printf 'Inventário SBOM';;
        *) printf '%s' "$1";;
    esac
}
progress_safe() {
    # JSON quoting removes terminal controls, including OSC/CSI and newlines.
    jq -aRn --arg value "$1" '$value'
}
progress_action() {
    local name
    case $1 in
        preparation) printf 'preparação do ambiente e verificação do toolchain exigido';;
        geiger) printf 'análise dos membros selecionados do workspace e validação dos relatórios';;
        rust-test) printf 'testes do workspace Rust selecionado';;
        rust-build) printf 'compilação do workspace Rust selecionado';;
        rust-check|rust-clippy|rust-fmt) printf 'verificação estática do workspace Rust selecionado';;
        sdd-structure) printf 'validação estrutural dos artefatos SDD';;
        ox) printf 'validação das autoridades e contratos de governança Ox';;
        governance-tests) printf 'testes dos contratos de governança';;
        scripts-tests) printf 'testes dos scripts de automação';;
        scripts-syntax) printf 'verificação de sintaxe dos scripts';;
        coverage) printf 'medição de cobertura do workspace selecionado';;
        sbom) printf 'inventário dos componentes selecionados';;
        *)
           # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
           name=$(progress_name "$1") || return 2
           printf 'verificação %s sobre as entradas selecionadas' "${name}";;
    esac
}
progress_duration() { printf '%02d:%02d' "$(($1/60))" "$(($1%60))"; }
progress_init() {
    PROGRESS_RUN=$1 PROGRESS_TOTAL=$(($2+2)) PROGRESS_DONE=0 PROGRESS_INDEX=0
    PROGRESS_STARTED=${SECONDS} PROGRESS_ACTIVE=false PROGRESS_CANCELLED=false
    PROGRESS_ID='' PROGRESS_WATCH='' PROGRESS_LAST=0 PROGRESS_TTY=false
    PROGRESS_REFERENCES=() PROGRESS_PUBLISHED=''
    [[ ! -t 2 ]] || PROGRESS_TTY=true
    PROGRESS_CONTROL=false
    if ${PROGRESS_TTY} && [[ ${TERM:-} != dumb ]]; then PROGRESS_CONTROL=true; fi
    PROGRESS_COLOR=false
    if ${PROGRESS_CONTROL} && [[ -z ${PROGRESS_USER_NO_COLOR:-} ]]; then PROGRESS_COLOR=true; fi
    OX_HUMAN_PROGRESS=true
    OX_EXECUTE_DEPTH=0
    progress_heading 'OX · AUTOMAÇÃO'
    printf '\n' >&2
    printf '  Progresso: fases com peso igual; membros Geiger + validação final quando observáveis. Conclusão não significa aprovação.\n' >&2
}
progress_begin() {
    local name action
    PROGRESS_ID=$1 PROGRESS_INDEX=$((PROGRESS_DONE+1)) PROGRESS_STARTED=${SECONDS}
    [[ $1 != finalization ]] || PROGRESS_INDEX=${PROGRESS_TOTAL}
    PROGRESS_ACTIVE=true PROGRESS_DIRECTORY=${2:-} PROGRESS_MEMBERS_MAX=0
    printf '\n' >&2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    name=$(progress_name "$1") || return 2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    action=$(progress_action "$1") || return 2
    progress_heading "[${PROGRESS_INDEX}/${PROGRESS_TOTAL}] ${name} ($1)"
    printf '\n' >&2
    progress_field 'Atividade:' "${action}"
    progress_line
    case $1 in preparation|finalization) progress_watch_start "$$";; *) :;; esac
}
progress_line() {
    local record=${1:-true} completed=0 total=0 phase=indisponível activity='executando' percent elapsed name row
    local observed=${PROGRESS_RUN}/progress-observed.json previous_phase previous_completed previous_percent
    if ${record} && [[ -f ${observed} ]]; then
        row=$(jq -r '[.phase,.completed,.percent]|@tsv' "${observed}") || return 2
        read -r previous_phase previous_completed previous_percent <<<"${row}"
        ((previous_percent<=PROGRESS_LAST)) || PROGRESS_LAST=${previous_percent}
        if [[ ${previous_phase} == "${PROGRESS_ID}" ]]; then PROGRESS_MEMBERS_MAX=${previous_completed}; fi
    fi
    if [[ ${PROGRESS_ID} == preparation ]]; then activity='ambiente e pré-requisitos'
    elif [[ ${PROGRESS_ID} == finalization ]]; then activity='resultados e publicação dos logs'
    elif [[ -f ${PROGRESS_DIRECTORY:-}/progress.json ]] &&
         jq -e '.schema==1 and .activity=="membros" and (.completed|type=="number" and floor==. and .>=0) and (.total|type=="number" and floor==. and .>0 and .<1000000) and .completed<=.total' "${PROGRESS_DIRECTORY}/progress.json" >/dev/null 2>&1; then
        row=$(jq -r '[.completed,.total]|@tsv' "${PROGRESS_DIRECTORY}/progress.json") || return 2
        read -r completed total <<<"${row}"
        ((completed>=PROGRESS_MEMBERS_MAX)) || completed=${PROGRESS_MEMBERS_MAX}
        PROGRESS_MEMBERS_MAX=${completed}
        phase=$((100*completed/(total+1)))%
        activity="membros: ${completed}/${total}; validação final pendente"
    fi
    if ((total>0)); then percent=$((100*(PROGRESS_DONE*(total+1)+completed)/(PROGRESS_TOTAL*(total+1))))
    else percent=$((100*PROGRESS_DONE/PROGRESS_TOTAL)); fi
    ((percent>=PROGRESS_LAST)) || percent=${PROGRESS_LAST}
    ((percent<100)) || percent=99
    PROGRESS_LAST=${percent}
    if ${record}; then
        jq -n --arg phase "${PROGRESS_ID}" --argjson completed "${PROGRESS_MEMBERS_MAX}" --argjson percent "${percent}" \
          '{phase:$phase,completed:$completed,percent:$percent}' >"${observed}.next"
        mv -- "${observed}.next" "${observed}"
    fi
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    elapsed=$(progress_duration "$((SECONDS-PROGRESS_STARTED))") || return 2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    name=$(progress_name "${PROGRESS_ID}") || return 2
    if ${PROGRESS_CONTROL}; then printf '\r\033[2K' >&2; fi
    if ${PROGRESS_TTY}; then
        # Keep the refreshed line short enough for ordinary 80-column terminals.
        # The permanent phase block carries the full phase name and activity.
        printf '[%d/%d] total: %d%% | fase: %s | decorrido: %s' \
          "${PROGRESS_INDEX}" "${PROGRESS_TOTAL}" "${percent}" "${phase}" "${elapsed}" >&2
        if ((total>0)); then printf ' | membros: %d/%d' "${completed}" "${total}" >&2; fi
    else
        printf '[%d/%d] %s (%s) | total: %d%% | fase: %s | atividade: %s | decorrido: %s' \
          "${PROGRESS_INDEX}" "${PROGRESS_TOTAL}" "${name}" "${PROGRESS_ID}" "${percent}" "${phase}" "${activity}" "${elapsed}" >&2
    fi
    if ! ${PROGRESS_CONTROL}; then printf '\n' >&2; fi
}
progress_watch_start() {
    local child=$1
    # The watcher owns and reaps its one timer. It never reads tool text.
    (
        local timer='' ticks=0 previous='' record=true
        # The initial finalization line already synchronized the counters. From
        # here retention owns the run, so its heartbeat must not read or write it.
        [[ ${PROGRESS_ID} != finalization ]] || record=false
        trap '[[ -z ${timer} ]] || { kill "$timer" 2>/dev/null || true; wait "$timer" 2>/dev/null || true; }; exit 0' TERM INT HUP
        while kill -0 "${child}" 2>/dev/null; do
            sleep 1 & timer=$!; wait "${timer}" || true; timer=''
            kill -0 "${child}" 2>/dev/null || break
            ticks=$((ticks+1))
            # TTY refreshes elapsed time; redirected output gets real events or
            # a thirty-second activity heartbeat, never a fabricated percentage.
            current=''
            if [[ -f ${PROGRESS_DIRECTORY:-}/progress.json ]]; then current=$(cat -- "${PROGRESS_DIRECTORY}/progress.json"); fi
            if ${PROGRESS_TTY} || [[ ${current} != "${previous}" ]] || ((ticks%30==0)); then progress_line "${record}"; fi
            previous=${current}
        done
    ) &
    PROGRESS_WATCH=$!
}
progress_watch_stop() {
    if [[ -n ${PROGRESS_WATCH:-} ]]; then
        kill -TERM "${PROGRESS_WATCH}" 2>/dev/null || true
        wait "${PROGRESS_WATCH}" 2>/dev/null || true
        PROGRESS_WATCH=''
    fi
    if ${PROGRESS_CONTROL:-false}; then printf '\r\033[2K' >&2; fi
}
progress_log_reference() {
    local path=$1 rel
    if [[ -n ${PROGRESS_PUBLISHED:-} && ${path} == "${PROGRESS_RUN}/"* ]]; then
        rel=${path#"${PROGRESS_RUN}/"}
        # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
        rel=$(log_name "${rel}") || return 2
        printf '%s/%s--%s.log' "${PROGRESS_PUBLISHED}" "${PROGRESS_RUN##*/}" "${rel}"
    else printf '%s' "${path}"; fi
}
progress_problem() {
    local number=$1 what=$2 where=$3 cause=$4 code=$5 diagnostic=$6 reference quoted
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    reference=$(progress_log_reference "${diagnostic}") || return 2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    quoted=$(progress_safe "${reference}") || return 2
    printf '%d. %s\n   Onde: %s.\n   Causa: %s.\n   Código: %s.\n   Diagnóstico: %s.\n' \
      "${number}" "${what}" "${where}" "${cause}" "${code}" "${quoted}" >&2
}
progress_cause() {
    # Only exact adapter-owned reasons are interpreted. Unknown/free text is not
    # echoed (it can contain secrets); source reports remain available for review.
    case ${2:-$1} in
        DATASET_INVALID) printf 'base de dados ausente, inválida, alterada ou vencida';;
        TOOL_UNAVAILABLE) printf 'ferramenta ou componente instalado exigido indisponível';;
        TOOL_CHANGED) printf 'identidade do executável mudou';;
        INPUT_INVALID) printf 'entradas, inventário ou snapshot inválidos ou alterados';;
        POLICY_INVALID) printf 'configuração, regras ou revisão de exceções inválidas';;
        EXECUTOR_INVALID) printf 'execução nativa ou diagnóstico de infraestrutura inválido';;
        REPORT_INVALID) printf 'relatório rejeitado ou incompatível com a execução';;
        UNKNOWN) printf 'causa não determinada';;
        'Required installed toolchain unavailable'|'Required installed Rust toolchain unavailable') printf 'toolchain Rust instalado exigido indisponível';;
        'Missing/invalid adapter assessment') printf 'assessment do adaptador ausente, inválido ou incompatível com o código observado';;
        'Incomplete Geiger member reports; all workspace members attempted'|'Incomplete Geiger report; raw omissions and diagnostics retained') printf 'relatório Geiger incompleto segundo o parser existente';;
        'Invalid/incomplete scanner report'|'Invalid/incomplete native report') printf 'relatório rejeitado pelo parser existente';;
        'Tool binary changed during check'|'Configured native executable changed after selection') printf 'identidade do executável mudou';;
        'Input/snapshot changed'|'Input/snapshot changed during check') printf 'entradas mudaram durante a verificação';;
        *) printf 'causa não determinada';;
    esac
}
progress_findings() {
    local directory=$1 code=$2 expected=${3:-0} report='' records='' record file line rule amount quoted_file n=0 displayed=0
    case ${PROGRESS_ID} in ruff|bandit|opengrep|gitleaks|history|shellcheck) :;; *) printf '0'; return;; esac
    for report in "${directory}/report.json" "${directory}/tool/stdout.log"; do
        if [[ -f ${report} ]] && strict_json "${report}" 2>/dev/null; then break; fi
        report=''
    done
    if [[ -z ${report} ]]; then printf '0'; return; fi
    # This function also runs in command substitution. Transfer selected raw
    # locators through an owned JSON file rather than losing them in a subshell.
    jq -n --arg report "${report}" '[$report]' >"${directory}/progress-references.json"
    # Metadata only: never render free-form messages, source/code, secret values,
    # snippets or fixes. Group identical location/rule records, preserving counts.
    records=$(jq -c --arg check "${PROGRESS_ID}" '
      def location($file;$line;$rule): {file:$file,line:$line,rule:$rule};
      (if $check=="ruff" and type=="array" then map(location(.filename;.location.row;.code))
       elif $check=="bandit" and (.results|type)=="array" then [.results[]|location(.filename;.line_number;.test_id)]
       elif $check=="opengrep" and (.results|type)=="array" then [.results[]|location(.path;.start.line;.check_id)]
       elif ($check=="gitleaks" or $check=="history") and type=="array" then map(location(.File;.StartLine;.RuleID))
       elif $check=="shellcheck" and type=="array" then map(location(.file;.line;("SC"+(.code|tostring))))
       else [] end) |
      map(select((.file|type)=="string" and (.file|length)>0 and (.file|length)<1024 and
        (.line|type)=="number" and (.line|floor)==.line and .line>0)) |
      group_by([.file,.line,.rule]) | .[] | .[0]+{count:length}
    ' "${report}" 2>/dev/null) || { printf '0'; return; }
    while IFS= read -r record; do
        [[ -n ${record} ]] || continue
        file=$(jq -r '.file' <<<"${record}"); line=$(jq -r '.line' <<<"${record}")
        rule=$(jq -r 'if (.rule|type)=="string" and (.rule|test("^[A-Za-z0-9_.-]{1,100}$")) then .rule else "identificador indisponível" end' <<<"${record}")
        amount=$(jq -r '.count' <<<"${record}"); n=$((n+1))
        displayed=$((displayed+amount))
        # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
        quoted_file=$(progress_safe "${file}") || return 2
        progress_problem "${n}" "Achado ${rule}; ocorrências relacionadas: ${amount}" "${PROGRESS_ID}, arquivo ${quoted_file}, linha ${line}" 'causa não determinada' "${code}" "${report}"
    done <<<"${records}"
    if [[ ${expected} =~ ^[0-9]+$ ]] && ((expected>displayed)); then
        n=$((n+1))
        progress_problem "${n}" "Achados adicionais sem localização extraível; quantidade: $((expected-displayed))" "fase ${PROGRESS_ID}, localização indisponível" 'causa não determinada' "${code}" "${report}"
    fi
    printf '%d' "${n}"
}
progress_governance_project() (
    # check-ox text v1 only. Bounded byte samples are disposable projections;
    # source logs are read-only. No stream ordering beyond stdout/stderr is claimed.
    local directory=$1 stream path sample bytes truncated row source target component current mode sample_sha
    local projection=${1}/.progress-governance-streams.json allowed=${1}/.progress-governance-sources.json
    local -a sources targets parts
    printf '[]\n' >"${projection}" || return 2
    for stream in stdout stderr; do
        path=${directory}/${stream}.log
        sample=${directory}/.progress-governance-${stream}.sample
        mode=0
        if [[ -f ${path} && ! -L ${path} ]]; then mode=$(stat -c '%a' -- "${path}") || return 2; fi
        if [[ -f ${path} && -r ${path} && ! -L ${path} ]] && (( (8#${mode} & 8#444) != 0 )); then
            head -c 65537 -- "${path}" >"${sample}" || return 2
            bytes=$(wc -c <"${sample}") || return 2
            truncated=false
            if ((bytes>65536)); then truncated=true; bytes=65536; fi
            # Materialize the bounded bytes so every producer failure is checked.
            head -c 65536 -- "${sample}" >"${sample}.bounded" || return 2
            mv -- "${sample}.bounded" "${sample}" || return 2
            sample_sha=$(sha256sum <"${sample}") || return 2
            sample_sha=${sample_sha:0:64}
            # jq replaces invalid UTF-8 with U+FFFD; rejecting every non-ASCII
            # record below makes that replacement explicit as unrecognized data.
            row=$(jq -Rsc --arg stream "${stream}" --arg path "${path}" \
                --argjson bytes "${bytes}" --argjson truncated "${truncated}" --arg sample_sha "${sample_sha}" '
              def safe:
                type=="string" and length>0 and length<=256 and
                test("^[A-Za-z0-9_./-]+(#[A-Za-z0-9_.-]+)?$") and
                (startswith("/")|not) and
                (test("secret|password|credential|token|api[_-]?key";"i")|not) and
                (split("/")|all(.[];length<=80));
              (if $truncated and (endswith("\n")|not) then split("\n")[:-1] else split("\n") end) |
              map(select(length>0)) |
              map(if test("^[\\x20-\\x7e]+$") and startswith("FAIL: Broken/escaping link: ") then
                ltrimstr("FAIL: Broken/escaping link: ") | split(": ") |
                if length==2 and (.[0]|safe) and (.[1]|safe) and
                  (.[0]|endswith(".md")) and (.[0]|split("/")|all(.[];.!="" and .!="." and .!="..")) and
                  (.[1]|split("#")[0]|endswith(".md") or endswith(".json"))
                then {source:.[0],target:.[1],known:true}
                else {source:null,target:null,known:true} end
              else {known:false} end) as $records |
              {stream:$stream,path:$path,status:(if $bytes>0 then "nonempty" else "empty" end),
               bytes_read:$bytes,truncated:$truncated,sample_sha256:$sample_sha,
               raw_sha256:(if $truncated then null else $sample_sha end),
               recognized:([$records[]|select(.known)]|length),
               unknown_records:([$records[]|select(.known|not)]|length),
               unsafe_fields:0,groups:[$records[]|select(.known)|{source,target,count:1}]}
            ' <"${sample}") || return 2
            rm -f -- "${sample}"
        else
            row=$(jq -cn --arg stream "${stream}" --arg path "${path}" \
              '{stream:$stream,path:$path,status:"unavailable",bytes_read:0,truncated:false,sample_sha256:null,raw_sha256:null,recognized:0,unknown_records:0,unsafe_fields:0,groups:[]}') || return 2
        fi
        # Validate parsed source metadata against repository-owned ordinary paths.
        # Unknown source names are never emitted, even when syntactically valid.
        printf '[]\n' >"${allowed}" || return 2
        capture_lines sources jq -r '[.groups[].source|select(.!=null)]|unique[]' <<<"${row}" || return 2
        for source in "${sources[@]}"; do
            # shellcheck disable=SC2153 # ROOT is initialized by common.sh; lowercase root is a different local.
            current=${ROOT}
            IFS=/ read -ra parts <<<"${source}"
            for component in "${parts[@]}"; do
                current=${current}/${component}
                [[ ! -L ${current} ]] || break
            done
            if [[ ${current} == "${ROOT}/${source}" && -f ${current} && ! -L ${current} ]]; then
                # $source is a jq variable bound by --arg, not shell interpolation.
                # shellcheck disable=SC2016
                capture_lines targets jq -r --arg source "${source}" '[.groups[]|select(.source==$source)|.target]|unique[]' <<<"${row}" || return 2
                for target in "${targets[@]}"; do
                    # A forged log cannot introduce arbitrary credential-shaped
                    # path text: the exact inline destination must occur locally.
                    # Unsupported Markdown forms conservatively hide both fields.
                    if grep -Fq -- "](${target})" "${current}"; then
                        jq --arg source "${source}" --arg target "${target}" '.+[{source:$source,target:$target}]' "${allowed}" >"${allowed}.next" || return 2
                        mv -- "${allowed}.next" "${allowed}" || return 2
                    fi
                done
            fi
        done
        row=$(jq -c --slurpfile allowed "${allowed}" '
          .groups |= (map(. as $group | if .source!=null and any($allowed[0][];.source==$group.source and .target==$group.target) then . else .source=null|.target=null end)) |
          .unsafe_fields=([.groups[]|select(.source==null)]|length) |
          .groups |= (group_by([.source,.target]) | map(.[0]+{count:length}) | group_by(.source) |
            . as $files | ([.[]|length]|max//0) as $longest |
            [range(0;$longest) as $i | $files[] | .[$i]//empty])
        ' <<<"${row}") || return 2
        jq --argjson row "${row}" '.+[$row]' "${projection}" >"${projection}.next" || return 2
        mv -- "${projection}.next" "${projection}" || return 2
    done
    jq -c '
      . as $streams | [ .[]|select(.recognized>0)|.stream ] as $known |
      (if ($known|length)>0 then $known else [.[]|select(.status=="nonempty")|.stream] end) as $selected |
      reduce $streams[] as $stream ({remaining:10,streams:[]};
        ($stream.groups[:.remaining]) as $visible |
        .streams += [$stream+{display_groups:$visible,
          omitted_groups:(($stream.groups|length)-($visible|length)),
          omitted_occurrences:([$stream.groups[($visible|length):][].count]|add//0)}] |
        .remaining-=($visible|length)) |
      {schema:1,parser:"check-ox-broken-link-v1",
       limits:{bytes_per_stream:65536,groups:10,field_characters:256},selected:$selected,streams:.streams}
    ' "${projection}" || return 2
    rm -f -- "${projection}" "${allowed}"
)
progress_governance() {
    local projection=$1 code=$2 row stream recognized unknown truncated unavailable omitted amount source target quoted_source quoted_target reference n=0
    local -a rows groups
    capture_lines rows jq -c '.streams[]' "${projection}" || return 2
    for row in "${rows[@]}"; do
        stream=$(jq -r '.stream' <<<"${row}") || return 2
        recognized=$(jq -r '.recognized' <<<"${row}") || return 2
        unknown=$(jq -r '.unknown_records' <<<"${row}") || return 2
        truncated=$(jq -r '.truncated' <<<"${row}") || return 2
        unavailable=$(jq -r '.status' <<<"${row}") || return 2
        reference=${projection%/*}/${stream}.log
        amount=${recognized}
        if [[ ${truncated} == true ]]; then amount="ao menos ${recognized}"; fi
        printf '    Diagnóstico Ox (%s): links quebrados/fora do limite: %s; registros não reconhecidos: %s.\n' "${stream}" "${amount}" "${unknown}" >&2 || return 2
        if [[ ${unavailable} == unavailable ]]; then
            printf '    Limitação (%s): stream ausente ou ilegível; captura disponível não confirmada.\n' "${stream}" >&2 || return 2
        elif [[ ${unavailable} == empty ]]; then
            printf '    Limitação (%s): stream vazio; diagnóstico indisponível.\n' "${stream}" >&2 || return 2
        fi
        if [[ ${truncated} == true ]]; then
            printf '    Limitação (%s): leitura truncada em 65536 bytes; contagens são limites inferiores; fragmento final incompleto omitido.\n' "${stream}" >&2 || return 2
        fi
        if ((unknown>0)); then printf '    Limitação (%s): formato/encoding/controles não reconhecidos; causa não determinada para esses registros.\n' "${stream}" >&2 || return 2; fi
        capture_lines groups jq -c '.display_groups[]' <<<"${row}" || return 2
        local group
        for group in "${groups[@]}"; do
            n=$((n+1))
            source=$(jq -r '.source//"indisponível"' <<<"${group}") || return 2
            target=$(jq -r '.target//"indisponível"' <<<"${group}") || return 2
            amount=$(jq -r '.count' <<<"${group}") || return 2
            # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
            quoted_source=$(progress_safe "${source}") || return 2
            # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
            quoted_target=$(progress_safe "${target}") || return 2
            # shellcheck disable=SC2310 # The diagnostic formatter propagates encoding/output failure.
            progress_problem "${n}" "Link quebrado/fora do limite; ocorrências relacionadas: ${amount}"               "Ox, ${stream}, arquivo ${quoted_source}, alvo ${quoted_target}"               'referência local rejeitada pelo checker; origem exata não determinada' "${code}" "${reference}" || return 2
        done
        omitted=$(jq -r '.omitted_groups' <<<"${row}") || return 2
        amount=$(jq -r '.omitted_occurrences' <<<"${row}") || return 2
        if ((omitted>0)); then
            printf '    Omissões (%s): %s grupos, %s ocorrências; identidades seguras no relatório de projeção; bruto preservado.\n' "${stream}" "${omitted}" "${amount}" >&2 || return 2
        fi
        amount=$(jq -r '.unsafe_fields' <<<"${row}") || return 2
        if ((amount>0)); then printf '    Limitação (%s): campos indisponíveis por segurança/ambiguidade em %s ocorrências.\n' "${stream}" "${amount}" >&2 || return 2; fi
    done
    printf '%d' "${n}"
}

progress_end() {
    local result=$1 assessment=${2:-} state code tool_code reason_code='' reason='' count='' label summary diagnostic duration name action reference quoted cause n=0 governance_projection=''
    progress_watch_stop
    if [[ -f ${PROGRESS_DIRECTORY:-}/progress.json ]]; then progress_line; progress_watch_stop; fi
    state=$(jq -r '.state//"error"' "${result}")
    code=$(jq -r '.exit_code//2' "${result}")
    tool_code=$(jq -r '(.tool_exit_code//.exit_code//2)|if type=="number" and floor==. and .>=0 and .<=255 then . else 2 end' "${result}")
    reason=$(jq -r '.reason//""' "${result}")
    diagnostic=${result}
    if [[ -s ${result%/*}/stderr.log ]]; then diagnostic=${result%/*}/stderr.log
    elif [[ -s ${result%/*}/stdout.log ]]; then diagnostic=${result%/*}/stdout.log; fi
    if [[ -n ${assessment} && -f ${assessment} ]]; then
        reason=$(jq -r '.reason//""' "${assessment}")
        reason_code=$(jq -r '.reason_code//""' "${assessment}")
        count=$(jq -r 'if (.finding_count|type)=="number" then .finding_count else empty end' "${assessment}")
        diagnostic=${assessment}
    fi
    if [[ ${PROCESS_CANCELLED:-false} == true || ${PROGRESS_CANCELLED} == true ]]; then state=cancelled; PROGRESS_CANCELLED=true; fi
    # Parse only this check's known text format; raw/result and exit remain intact.
    if [[ ${PROGRESS_ID} == ox && ${state} != passed && ${state} != recorded && ${state} != skipped && ${state} != skip ]]; then
        governance_projection=${result%/*}/progress-governance.json
        # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
        if progress_governance_project "${result%/*}" >"${governance_projection}.next" 2>/dev/null; then
            mv -- "${governance_projection}.next" "${governance_projection}"
            diagnostic=$(jq -r --arg directory "${result%/*}" 'if (.selected|length)>0 then $directory+"/"+.selected[0]+".log" else $directory+"/result.json" end' "${governance_projection}") || return 2
            PROGRESS_REFERENCES+=("${governance_projection}")
        else
            rm -f -- "${governance_projection}.next"
            governance_projection=''
            diagnostic=${result}
        fi
        # Retain both streams, including unrecognized records; no cross-stream
        # chronological order is inferred. Publication verifies their locators.
        local stream_path
        for stream_path in "${result%/*}/stdout.log" "${result%/*}/stderr.log"; do
            [[ ! -f ${stream_path} ]] || PROGRESS_REFERENCES+=("${stream_path}")
        done
    fi
    case ${state} in
        passed) label=SUCESSO; summary='execução concluída sem falha reportada';;
        recorded) label=REGISTRADO; summary='medição ou inventário registrado; não representa aprovação';;
        findings) label=FALHA; summary="achados reportados: ${count:-quantidade indisponível}";;
        blocked) label=BLOQUEADA; summary='pré-requisito ou entrada exigida impediu a execução';;
        skipped|skip) label=IGNORADA; summary='execução ignorada conforme estado registrado';;
        cancelled) label=CANCELADA; summary='interrupção observada; execução parcial';;
        *) label=FALHA; summary='falha de execução ou relatório inválido';;
    esac
    if [[ -n ${governance_projection} && ${state} != cancelled && ${state} != blocked ]]; then
        summary='checker Ox terminou com falha; consulte os diagnósticos e limites'
    fi
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    duration=$(progress_duration "$((SECONDS-PROGRESS_STARTED))") || return 2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    name=$(progress_name "${PROGRESS_ID}") || return 2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    action=$(progress_action "${PROGRESS_ID}") || return 2
    progress_phase_result "${name}" "${duration}" "${label}"
    progress_field 'Executado:' "${action}."
    progress_field 'Resultado:' "${summary}."
    if [[ ${state} == skipped || ${state} == skip ]]; then progress_field WARNING 'Execução IGNORADA; motivo detalhado no resultado registrado.'; fi
    if [[ -n ${assessment} && -f ${assessment} ]]; then
        local warnings skips limits
        warnings=$(jq -r 'if (.warnings|type)=="array" then .warnings|length else "indisponível" end' "${assessment}")
        skips=$(jq -r 'if (.skips|type)=="array" then .skips|length else "indisponível" end' "${assessment}")
        limits=$(jq -r 'if (.limits|type)=="array" then .limits|length else "indisponível" end' "${assessment}")
        if [[ ${warnings} =~ ^[0-9]+$ && ${warnings} -gt 0 ]] || [[ ${skips} =~ ^[0-9]+$ && ${skips} -gt 0 ]]; then
            progress_field WARNING 'Avisos ou skips registrados; consulte o relatório.'
        fi
        if [[ ${warnings} != indisponível || ${skips} != indisponível ]]; then
            printf '    Avisos: %s; skips registrados: %s (consulte o relatório).\n' "${warnings}" "${skips}" >&2
        fi
        if [[ ${limits} != indisponível ]]; then
            printf '    Limitações registradas: %s (consulte o relatório).\n' "${limits}" >&2
        fi
        if jq -e '.limits|type=="array" and index("Offline flags are not OS isolation.")!=null' "${assessment}" >/dev/null 2>&1; then
            printf '    Limitação: flags offline não garantem isolamento do sistema operacional.\n' >&2
        fi
        if jq -e '.limits|type=="array" and index("Generated directories and historical validation excluded; history is separate.")!=null' "${assessment}" >/dev/null 2>&1; then
            printf '    Escopo: diretórios gerados e validações históricas excluídos; histórico verificado separadamente.\n' >&2
        fi
    fi
    PROGRESS_REFERENCES+=("${diagnostic}")
    [[ ! -f ${result%/*}/report.json ]] || PROGRESS_REFERENCES+=("${result%/*}/report.json")
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    reference=$(progress_log_reference "${diagnostic}") || return 2
    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
    quoted=$(progress_safe "${reference}") || return 2
    progress_field 'Log/relatorio:' "${quoted}"
    if [[ ${state} != passed && ${state} != recorded && ${state} != skipped && ${state} != skip ]]; then
        printf '\nProblemas:\n' >&2
        if [[ -n ${governance_projection} ]]; then
            # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
            n=$(progress_governance "${governance_projection}" "${tool_code}") || return 2
        elif [[ ${PROGRESS_ID} == ox ]]; then
            printf '    Limitação: parser de diagnóstico indisponível; causa não determinada; consulte o resultado e os streams brutos.\n' >&2
        fi
        if [[ ${state} == findings || ( ${count} =~ ^[0-9]+$ && ${count} -gt 0 ) ]]; then n=$(progress_findings "${result%/*}" "${tool_code}" "${count:-0}"); fi
        if [[ -f ${result%/*}/progress-references.json ]]; then
            local raw_reference
            local -a raw_references
            capture_nul raw_references jq -j '.[]|.,"\u0000"' "${result%/*}/progress-references.json" || return 2
            for raw_reference in "${raw_references[@]}"; do
                if [[ ${raw_reference} != "${result%/*}/report.json" ]]; then
                    PROGRESS_REFERENCES+=("${raw_reference}")
                fi
            done
        fi
        if ((n==0)) && [[ -n ${assessment} && -f ${assessment} ]] && jq -e '.member_results|type=="array" and any(.[];.state!="passed" and .state!="recorded")' "${assessment}" >/dev/null 2>&1; then
            local member member_state member_code member_reason member_manifest member_index=0
            local -a members
            capture_lines members jq -c '.member_results[]' "${assessment}" || return 2
            for member in "${members[@]}"; do
                member_state=$(jq -r '.state' <<<"${member}")
                if [[ ${member_state} != passed && ${member_state} != recorded ]]; then
                    n=$((n+1)); member_code=$(jq -r '.tool_exit_code//.exit_code' <<<"${member}")
                    member_reason=$(jq -r '.reason//""' <<<"${member}")
                    member_manifest=$(jq -r '.manifest//"localização indisponível"' <<<"${member}")
                    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
                    quoted=$(progress_safe "${member_manifest}") || return 2
                    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
                    cause=$(progress_cause "${member_reason}") || return 2
                    progress_problem "${n}" 'Análise do membro apresentou problemas' "Geiger, membro $((member_index+1)), manifesto ${quoted}" "${cause}" "${member_code}" "${result%/*}/tool/${member_index}/stdout.log"
                    # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
                    quoted=$(progress_safe "${result%/*}/tool/${member_index}/stderr.log") || return 2
                    printf '   Stderr: %s\n' "${quoted}" >&2
                    PROGRESS_REFERENCES+=("${result%/*}/tool/${member_index}/stdout.log" "${result%/*}/tool/${member_index}/stderr.log")
                fi
                member_index=$((member_index+1))
            done
        fi
        if ((n==0)) || [[ ${state} == blocked || ${state} == cancelled || ( -z ${governance_projection} && ( ${state} == error || ${state} == failed ) ) ]]; then
            local signal
            signal=$(jq -r 'if (.signal|IN("INT","TERM","HUP")) then .signal else empty end' "${result}")
            # shellcheck disable=SC2310 # The callee returns an explicit status; this branch propagates failure.
            cause=$(progress_cause "${reason}" "${reason_code:-${reason}}") || return 2
            progress_problem "$((n+1))" "${summary}" "fase ${PROGRESS_ID}${signal:+, sinal ${signal}}" "${cause}" "${tool_code}" "${diagnostic}"
        fi
    fi
    printf '    Limites: saída bruta não reproduzida no terminal; avisos e detalhes permanecem nos logs. A aceitação funcional do produto é avaliada separadamente.\n' >&2
    if [[ ${state} != cancelled ]]; then PROGRESS_DONE=$((PROGRESS_DONE+1)); fi
    PROGRESS_ACTIVE=false
}
