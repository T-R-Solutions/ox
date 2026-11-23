#!/usr/bin/env bash
# Run lifecycle owns publication, cleanup, signal handling and the final status.
# Presentation callbacks are provided by progress.sh; raw logs by common.sh.
# shellcheck disable=SC2154 # Runner and progress modules initialize shared run state.
finalize_run() {
    local original_code=$1 publication_code=0 publication_log published_result='' reference publication_capture_failed=false
    local final_signal_code=${PROCESS_SIGNAL_CODE:-0} name duration label quoted published_reference
    # execute consumes the signal while waiting for child cleanup. Its observed
    # signal still owns the public result, even if aggregation returned error=2.
    if ((final_signal_code==0)); then final_signal_code=${original_code}; fi
    # Finalization owns cleanup until publication returns. Signals record the
    # cancellation without abandoning the run or leaving the watcher alive.
    trap 'progress_watch_stop' EXIT
    trap 'PROGRESS_CANCELLED=true; final_signal_code=130' INT
    trap 'PROGRESS_CANCELLED=true; final_signal_code=143' TERM
    trap 'PROGRESS_CANCELLED=true; final_signal_code=129' HUP
    progress_watch_stop
    if ${PROGRESS_ACTIVE}; then
        name=$(progress_name "${PROGRESS_ID}") || exit 2
        duration=$(progress_duration "$((SECONDS-PROGRESS_STARTED))") || exit 2
        label=FALHA
        if ${PROGRESS_CANCELLED}; then label=CANCELADA; fi
        progress_phase_result "${name}" "${duration}" "${label}"
        progress_field 'Resultado:' 'fase interrompida antes de registrar resultado completo.'
    fi
    progress_begin finalization
    # shellcheck disable=SC2034 # progress.sh consumes this shared phase index during finalization.
    PROGRESS_INDEX=${PROGRESS_TOTAL}
    if ! publication_log=$(mktemp "${TMPDIR:-/tmp}/ox-publication-XXXXXXXX.log" 2>/dev/null); then
        publication_log=/dev/null
        publication_capture_failed=true
    fi
    # run_complete owns retention and removal. Its output is preserved on failure,
    # because that path can no longer be published by the failing publisher.
    run_complete "${PROGRESS_RUN}" >"${publication_log}" 2>&1 || publication_code=$?
    progress_watch_stop
    name=$(progress_name finalization) || exit 2
    duration=$(progress_duration "$((SECONDS-PROGRESS_STARTED))") || exit 2
    if ${publication_capture_failed}; then
        progress_phase_result "${name}" "${duration}" FALHA
        printf '    Problemas:\n1. Captura do diagnóstico de publicação indisponível.\n   Onde: preparação do arquivo temporário de diagnóstico.\n   Causa: não foi possível criar o arquivo de diagnóstico; causa subjacente não determinada.\n   Código: 2.\n   Diagnóstico bruto: indisponível; encerramento e publicação foram tentados.\n' >&2
        printf 'total: %d%% | Execução incompleta.\n' "${PROGRESS_LAST}" >&2
        exit 2
    fi
    if ((publication_code==0)); then
        published_result=$(find "${ROOT}/.local/logs" -mindepth 2 -maxdepth 2 -type f -name "${PROGRESS_RUN##*/}--results.json.log" -print -quit)
        if [[ -n ${published_result} && -f ${published_result} ]]; then PROGRESS_PUBLISHED=${published_result%/*}
        else publication_code=2; printf 'Publicação não confirmou results.json retido.\n' >>"${publication_log}"; fi
    fi
    if ((publication_code)); then
        progress_phase_result "${name}" "${duration}" FALHA
        progress_field 'Resultado:' 'publicação dos logs não confirmada.'
        printf 'Problemas:\n' >&2
        progress_problem 1 'Falha ao publicar os logs; diagnóstico emergencial preservado' 'publicação dos logs' 'causa não determinada' "${publication_code}" "${publication_log}"
        printf 'total: %d%% | Execução incompleta.\n' "${PROGRESS_LAST}" >&2
        exit 2
    fi
    # A successful publisher return alone cannot confirm every earlier locator.
    # Verify before claiming completion or printing any "Referência publicada".
    for reference in "${PROGRESS_REFERENCES[@]}" "${PROGRESS_RUN}/results.json"; do
        published_reference=$(progress_log_reference "${reference}") || exit 2
        if [[ ! -f ${published_reference} || -L ${published_reference} ]]; then
            progress_phase_result "${name}" "${duration}" FALHA
            progress_field 'Resultado:' 'publicação incompleta; uma referência retida não foi confirmada.'
            printf 'Referência não confirmada: ' >&2
            progress_safe "${published_reference}" >&2
            printf 'Referência retida disponível: ' >&2
            progress_safe "${published_result}" >&2
            printf 'Captura/publicação incompleta; total: %d%% | Execução incompleta.\n' "${PROGRESS_LAST}" >&2
            rm -f -- "${publication_log}"
            exit 2
        fi
    done
    rm -f -- "${publication_log}"
    label=SUCESSO
    if ${PROGRESS_CANCELLED}; then label=CANCELADA; fi
    progress_phase_result "${name}" "${duration}" "${label}"
    progress_field 'Executado:' 'finalização dos resultados e publicação dos logs.'
    quoted=$(progress_safe "${PROGRESS_PUBLISHED}") || exit 2
    progress_field 'Logs publicados:' "${quoted}"
    # Resolve every phase's earlier live temporary reference to a retained path.
    for reference in "${PROGRESS_REFERENCES[@]}" "${PROGRESS_RUN}/results.json"; do
        published_reference=$(progress_log_reference "${reference}") || exit 2
        quoted=$(progress_safe "${published_reference}") || exit 2
        printf 'Referência publicada: %s\n' "${quoted}" >&2
    done
    printf '\n' >&2
    progress_heading 'RESUMO DA EXECUÇÃO'
    printf '\n' >&2
    if ${PROGRESS_CANCELLED}; then
        progress_field WARNING 'Execução CANCELADA.'
        printf 'total: %d%% | Execução CANCELADA; fases restantes não executadas.\n' "${PROGRESS_LAST}" >&2
        original_code=${final_signal_code}
    else
        if ((original_code)); then progress_field FALHA "Uma ou mais fases falharam ou foram bloqueadas; código: ${original_code}."
        else progress_field SUCESSO 'Checks selecionados concluídos; consulte os estados e avisos.'; fi
        printf 'total: 100%% | Resultados registrados; consulte os estados de cada fase. A aceitação funcional do produto é avaliada separadamente.\n' >&2
    fi
    exit "${original_code}"
}
