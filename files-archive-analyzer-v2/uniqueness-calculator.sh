#!/usr/bin/env bash
set -euo pipefail

FILE1="${1:?Usage: $0 file1 file2}"
FILE2="${2:?Usage: $0 file1 file2}"

FILE1_DIFF="${FILE1}-diff"
FILE2_DIFF="${FILE2}-diff"

awk '
    NR == FNR {
        hash = $1
        sub(/^>/, "", hash)
        hashes[hash] = 1
        next
    }
    {
        hash = $1
        sub(/^>/, "", hash)
        if (!(hash in hashes)) print
    }
' "$FILE2" "$FILE1" > $FILE1_DIFF

awk '
    NR == FNR {
        hash = $1
        sub(/^>/, "", hash)
        hashes[hash] = 1
        next
    }
    {
        hash = $1
        sub(/^>/, "", hash)
        if (!(hash in hashes)) print
    }
' "$FILE1" "$FILE2" > $FILE2_DIFF

echo "------------------"
echo "Differences saved:"
echo "  ${FILE1_DIFF}: entries only in $FILE1"
echo "  ${FILE2_DIFF}: entries only in $FILE2"
