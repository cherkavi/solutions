#!/usr/bin/env bash
set -euo pipefail

LIST="${1:?Usage: $0 diff_file}"

FOUND=0
MISSING=0

while IFS= read -r LINE || [[ -n "$LINE" ]]; do
    [[ "$LINE" =~ ^[[:space:]]*$ ]] && continue

    # Parse MD5 hash, filename, and remaining directory path
    HASH="${LINE%%[[:space:]]*}"
    REST="${LINE#"$HASH"}"
    REST="${REST#"${REST%%[![:space:]]*}"}"

    FILE="${REST%%[[:space:]]*}"
    DIR="${REST#"$FILE"}"
    DIR="${DIR#"${DIR%%[![:space:]]*}"}"

    SRC="${DIR%/}/$FILE"

    if [[ -f "$SRC" ]]; then
        ((FOUND += 1))
        printf 'OK:      %s\n' "$SRC"
    else
        ((MISSING += 1))
        printf 'MISSING: %s\n' "$SRC"
    fi
done < "$LIST"

printf '\nSummary: %d found, %d missing\n' "$FOUND" "$MISSING"

(( MISSING == 0 ))