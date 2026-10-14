#!/usr/bin/env bash
set -euo pipefail

LIST="${1:?Usage: $0 diff_file destination}"
DEST="${2:?Usage: $0 diff_file destination}"

mkdir -p -- "$DEST"

while IFS= read -r LINE || [[ -n "$LINE" ]]; do
    [[ "$LINE" =~ ^[[:space:]]*$ ]] && continue

    # Parse: MD5 HASH, FILENAME, DIRECTORY PATH
    HASH="${LINE%%[[:space:]]*}"
    REST="${LINE#"$HASH"}"
    REST="${REST#"${REST%%[![:space:]]*}"}"

    FILE="${REST%%[[:space:]]*}"
    DIR="${REST#"$FILE"}"
    DIR="${DIR#"${DIR%%[![:space:]]*}"}"

    SRC="${DIR%/}/$FILE"
    REL="${SRC#./}"
    TARGET="$DEST/$REL"

    if [[ -f "$SRC" ]]; then
        mkdir -p -- "$(dirname -- "$TARGET")"
        if cp --update=none -- "$SRC" "$TARGET"; then
            printf 'Copied: %s\n' "$SRC"
        fi
    else
        printf 'Missing: %s\n' "$SRC" >&2
    fi
done < "$LIST"