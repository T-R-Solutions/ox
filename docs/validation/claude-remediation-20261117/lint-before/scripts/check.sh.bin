#!/usr/bin/env bash
# Syntax validation only; does not execute the checked scripts.
set -euo pipefail
directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
listing=$(mktemp)
trap 'rm -f -- "${listing}"' EXIT
find "${directory}" -type f -name '*.sh' -print0 >"${listing}"
while IFS= read -r -d '' script; do
    bash -n "${script}"
done <"${listing}"
