#!/bin/bash

# Configuration
ANKI_URL="http://localhost:8765"
DECK_NAME="English"

mkdir -p decks/$DECK_NAME

# Helper function to invoke AnkiConnect via curl and jq
anki_invoke() {
    local action="$1"
    local params="$2"
    
    jq -n \
        --arg action "$action" \
        --argjson params "$params" \
        '{action: $action, params: $params, version: 6}' | \
    curl -s -X POST -H "Content-Type: application/json" -d @- "$ANKI_URL"
}

echo "Searching for cards in deck: '$DECK_NAME'..."

# Step 1: Find all card IDs in the specified deck
QUERY="deck:\"$DECK_NAME\""
PARAMS=$(jq -n --arg query "$QUERY" '{query: $query}')

RESPONSE=$(anki_invoke "findCards" "$PARAMS")
ERROR=$(echo "$RESPONSE" | jq -r '.error')

if [ "$ERROR" != "null" ] && [ -n "$ERROR" ]; then
    echo "Error from AnkiConnect: $ERROR"
    exit 1
fi

# Extract card IDs into a bash array
mapfile -t CARD_IDS < <(echo "$RESPONSE" | jq -r '.result[]')
TOTAL_CARDS=${#CARD_IDS[@]}

if [ "$TOTAL_CARDS" -eq 0 ]; then
    echo "No cards found in deck '$DECK_NAME'."
    exit 0
fi

echo "Found $TOTAL_CARDS cards. Retrieving details and starting loop..."
echo "----------------------------------------"

# Step 2: Fetch info for all cards at once
CARDS_PARAMS=$(jq -n --argjson cards "$(printf '%s\n' "${CARD_IDS[@]}" | jq -R . | jq -s .)" '{cards: $cards}')
CARDS_INFO_RESPONSE=$(anki_invoke "cardsInfo" "$CARDS_PARAMS")

# Step 3: Loop through each card using jq iteration
echo "$CARDS_INFO_RESPONSE" | jq -c '.result[]' | while read -r card; do
    CARD_ID=$(echo "$card" | jq -r '.cardId')
    # QUESTION=$(echo "$card" | jq -r '.question' | sed 's/<[^>]*>/ /g' | xargs) # Strip HTML tags for clean terminal print
    # ANSWER=$(echo "$card" | jq -r '.answer' | sed 's/<[^>]*>/ /g' | xargs) # Strip HTML tags for clean terminal print
    QUESTION=$(echo "$card" | jq -r '.fields.Front.value' ) 
    ANSWER=$(echo "$card" | jq -r '.fields.Back.value' )
    
    echo "Card ID: $CARD_ID"
    echo "Front:   $QUESTION"
    echo "Back:    $ANSWER"
    echo "$card"
    echo "----------------------------------------"

    json_string=$(echo "$card" | jq -c '{
        card_id: .cardId, 
        question: (.fields.Front.value // ""), 
        answer: (.fields.Back.value // "")
    }')

    echo $json_string > decks/$DECK_NAME/$CARD_ID.json

done