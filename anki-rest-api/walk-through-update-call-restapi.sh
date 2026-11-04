for JSON_FILE in decks/"$DECK_NAME"/*.json.update; do
    echo "----------------------"
    echo $JSON_FILE
    # JSON_FILE=decks/English/1793244662881.json.update

    # Extract variables from the JSON using jq
    CARD_ID=$(jq -r '.card_id' "$JSON_FILE")
    QUESTION=$(jq -r '.question' "$JSON_FILE")
    QUESTION_SENTENCE=$(jq -r '.question_sentence' "$JSON_FILE")
    ANSWER=$(jq -r '.answer' "$JSON_FILE")
    # Construct the Front field string
    FRONT="-> $QUESTION <br>$QUESTION_SENTENCE"

    NOTE_ID=$(curl -s localhost:8765 -X POST -d "{
        \"action\": \"cardsInfo\",
        \"params\": { \"cards\": [$CARD_ID] },
        \"version\": 6
    }" | jq '.result[0].note')
    echo $NOTE_ID

    # 2. Update the note fields using that note ID
    curl -s localhost:8765 -X POST -d "$(jq -n \
        --argjson id "$NOTE_ID" \
        --arg front "$FRONT" \
        --arg back "$ANSWER" \
        '{
            action: "updateNoteFields",
            version: 6,
            params: {
                note: {
                    id: $id,
                    fields: {
                        Front: $front,
                        Back: $back
                    }
                }
            }
        }')"

done
