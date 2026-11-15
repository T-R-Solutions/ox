#!/usr/bin/env bash
# Inspect or apply the two-date log retention policy.
source "$(dirname -- "${BASH_SOURCE[0]}")/lib/common.sh"
action=inspect
while (($#)); do
    case $1 in
        --root) ROOT=$2; shift 2;;
        --apply) action=prune; shift;;
        --path) local_path "$2"; exit;;
        --help|-h) printf 'Usage: local.sh [--root ROOT] [--apply | --path runs|datasets|cargo]\n'; exit;;
        *) die "Unknown argument: $1";;
    esac
done
# shellcheck source=lib/logs.sh
source "${LIB_DIR}/logs.sh"
apply=false; [[ ${action} != prune ]] || apply=true
retain_logs "${ROOT}" "" "${apply}"
