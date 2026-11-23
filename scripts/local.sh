#!/usr/bin/env bash
# Inspect or apply the two-date log retention policy.
source "$(dirname -- "${BASH_SOURCE[0]}")/lib/common.sh"
main() {
    local action=inspect category='' action_seen=false
    while (($#)); do
        case $1 in
            --root|--path)
                (($#>=2)) && [[ -n $2 && $2 != --* ]] || die "Missing value: $1"
                if [[ $1 == --root ]]; then ROOT=$2
                else
                    [[ ${action_seen} == false ]] || die 'Choose --apply or --path once'
                    action_seen=true; action=path; category=$2
                fi
                shift 2;;
            --apply)
                [[ ${action_seen} == false ]] || die 'Choose --apply or --path once'
                action_seen=true; action=prune; shift;;
            --help|-h) printf 'Usage: local.sh [--root ROOT] [--apply | --path runs|datasets|cargo]\n'; return 0;;
            *) die "Unknown argument: $1";;
        esac
    done
    ROOT=$(cd -- "${ROOT}" && pwd -P) || die 'Repository root missing'
    if [[ ${action} == path ]]; then local_path "${category}"; return; fi
    # shellcheck source=lib/logs.sh
    source "${LIB_DIR}/logs.sh"
    local apply=false
    [[ ${action} != prune ]] || apply=true
    retain_logs "${ROOT}" "" "${apply}"
}
main "$@"
