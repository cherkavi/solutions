#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <source_dir> <destination_dir> <missing_files.txt>" >&2
    exit 1
fi

SOURCE_DIR="${1%/}"
DEST_DIR="${2%/}"
MISSING_FILE="$3"

if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "ERROR: Source directory does not exist: $SOURCE_DIR" >&2
    exit 1
fi

if [[ ! -f "$MISSING_FILE" ]]; then
    echo "ERROR: Missing files list not found: $MISSING_FILE" >&2
    exit 1
fi

mkdir -p "$DEST_DIR"

while read -r md5 filename relative_dir || [[ -n "${md5:-}" ]]; do
    [[ -z "${md5:-}" ]] && continue

    relative_dir="${relative_dir:-.}"
    relative_dir="${relative_dir%/}"

    # Absolute directory paths are used directly.
    if [[ "$relative_dir" == /* ]]; then
        source="$relative_dir/$filename"
    else
        source="$SOURCE_DIR/${relative_dir#./}/$filename"
        [[ "$relative_dir" == "." ]] && source="$SOURCE_DIR/$filename"
    fi

    if [[ -f "$source" ]]; then
        cp --update=none -- "$source" "$DEST_DIR/$filename"
        echo "Copied: $source -> $DEST_DIR/$filename"
    else
        echo "WARNING: File not found: $source" >&2
    fi
done < "$MISSING_FILE"

echo "Done. Files copied to: $DEST_DIR"