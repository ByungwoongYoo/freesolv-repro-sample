#!/usr/bin/env bash
# Download pinned FreeSolv v0.52 (if missing) and regenerate KEY_TABLE.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
COMMIT="6c7d19b4b565537365ffd22006aa2cd4643200c6"
URL="https://raw.githubusercontent.com/MobleyLab/FreeSolv/${COMMIT}/database.txt"
RAW="${ROOT}/data/database.txt"
PINNED_SHA="2d13f095713bc39b85f85dd7b4e5483fbb12fc694bf253bb1d92a4c4d484f260"

mkdir -p "${ROOT}/data" "${ROOT}/expected"

if [[ ! -f "${RAW}" ]]; then
  echo "Downloading FreeSolv database.txt @ ${COMMIT:0:7} ..."
  curl -fsSL -o "${RAW}" "${URL}"
fi

GOT="$(sha256sum "${RAW}" | awk '{print $1}')"
if [[ "${GOT}" != "${PINNED_SHA}" ]]; then
  echo "ERROR: sha256 mismatch for database.txt" >&2
  echo "  got:    ${GOT}" >&2
  echo "  expect: ${PINNED_SHA}" >&2
  exit 1
fi

python3 "${ROOT}/scripts/reproduce_split_table.py" "${RAW}" "${ROOT}/expected"
echo "OK — see expected/KEY_TABLE.md and expected/baseline_results.json"
