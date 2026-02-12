#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MERGER="$ROOT_DIR/merge_config.py"

if [[ ! -f "$MERGER" ]]; then
  printf 'merge_config.py not found: %s\n' "$MERGER" >&2
  exit 2
fi

merge_one() {
  local base_file="$1"
  local local_file="$2"
  local out_file="$3"
  shift 3

  python3 "$MERGER" \
    --base "$base_file" \
    --local "$local_file" \
    --out "$out_file" \
    --missing-local-ok \
    "$@"
}

merge_one \
  "$ROOT_DIR/opencode.base.jsonc" \
  "$ROOT_DIR/opencode.local.jsonc" \
  "$ROOT_DIR/opencode.jsonc" \
  "$@"

merge_one \
  "$ROOT_DIR/oh-my-opencode.base.jsonc" \
  "$ROOT_DIR/oh-my-opencode.local.jsonc" \
  "$ROOT_DIR/oh-my-opencode.jsonc" \
  "$@"

printf 'Generated opencode.jsonc and oh-my-opencode.jsonc\n'
