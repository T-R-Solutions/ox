#!/usr/bin/env bash
set -euo pipefail
source scripts/lib/common.sh
source scripts/lib/files.sh
out=docs/validation/toolbox-operational-completion
repo=.local/build/toolbox-completion/rustsec-official
{ git -C "$repo" remote -v; git -C "$repo" log -1 --format=fuller; git -C "$repo" fsck --full; git -C "$repo" status --porcelain; cargo-audit --version; cargo-deny --version; } > "$out/rustsec-inspection.txt" 2>&1
mkdir -p .local/build/toolbox-completion/import
# retain independent acquired checkout; preparation copies only reviewed content
cp -a "$repo" .local/build/toolbox-completion/import/rustsec
sha=$(tree_identity .local/build/toolbox-completion/import/rustsec)
revision=$(git -C "$repo" rev-parse HEAD)
published=$(git -C "$repo" show -s --format=%cs HEAD)
expiry=$(date -ud "$published +5 days" +%F)
jq -n --arg sha "$sha" --arg revision "$revision" --arg published "$published" --arg expiry "$expiry" '{rustsec:{source:"https://github.com/RustSec/advisory-db.git",license:"CC0-1.0 AND CC-BY-4.0 (retain upstream record attribution)",revision:$revision,dataset_date:$published,valid_until:$expiry,sha256:$sha,reviewer:"Codex authorized operational completion",provenance:"Fresh official clone, immutable HEAD, git fsck full; no signature claim"}}' > "$out/rustsec-review.json"
bash scripts/security/prepare-datasets.sh --review "$out/rustsec-review.json" --import .local/build/toolbox-completion/import --only rustsec > "$out/rustsec-prepare.stdout" 2> "$out/rustsec-prepare.stderr"
