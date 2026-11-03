#!/usr/bin/env bash
set -euo pipefail

LIST="${1:?Usage: $0 diff_file destination}"
DEST="${2:?Usage: $0 diff_file destination}"

mkdir -p -- "$DEST"

while IFS=$'\t' read -r HASH FILE DIR || [[ -n "${HASH:-}" ]]; do
    [[ -z "${HASH:-}" || -z "${FILE:-}" || -z "${DIR:-}" ]] && continue

    SRC="${DIR%/}/$FILE"
    REL="${SRC#./}"

    if [[ -f "$SRC" ]]; then
        mkdir -p -- "$DEST/$(dirname -- "$REL")"
        cp --update=none -- "$SRC" "$DEST/$REL"
        printf 'Copied: %s\n' "$SRC"
    else
        printf 'Missing: %s\n' "$SRC" >&2
    fi
done < "$LIST"
