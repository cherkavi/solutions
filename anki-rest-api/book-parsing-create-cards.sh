#!/bin/bash

# Path to your JSON file
JSON_FILE=$1
ANKI_URL="http://localhost:8765"
DECK_NAME="France" # Change this to your target deck name

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed." >&2
    exit 1
fi

# Check if the JSON file exists
if [ ! -f "$JSON_FILE" ]; then
    echo "Error: File $JSON_FILE not found." >&2
    exit 1
fi

# Read the JSON array and loop through each object
jq -c '.[]' "$JSON_FILE" | while read -r item; do
    # Extract fields using jq
    france=$(echo "$item" | jq -r '.france')
    german=$(echo "$item" | jq -r '.german')
    sentence_france=$(echo "$item" | jq -r '.sentence_france')
    sentence_german=$(echo "$item" | jq -r '.sentence_german')

    # Format the Front and Back HTML content
    # Using <br><br> to separate vocabulary from the example sentences
    FRONT_HTML="$france<br><br>$sentence_france"
    BACK_HTML="$german<br><br>$sentence_german"

    # Construct the AnkiConnect payload for adding a note
    PAYLOAD=$(jq -n \
        --arg deck "$DECK_NAME" \
        --arg front "$FRONT_HTML" \
        --arg back "$BACK_HTML" \
        '{
            action: "addNote",
            version: 6,
            params: {
                note: {
                    deckName: $deck,
                    modelName: "Basic",
                    fields: {
                        Front: $front,
                        Back: $back
                    },
                    options: {
                        allowDuplicate: false
                    }
                }
            }
        }')

    # Send the request to AnkiConnect
    RESPONSE=$(curl -s "$ANKI_URL" -X POST -d "$PAYLOAD")
    
    # Check for errors in the response
    ERROR=$(echo "$RESPONSE" | jq -r '.error')
    if [ "$ERROR" != "null" ]; then
        echo "Failed to add '$france': $ERROR"
    else
        echo "Successfully added: $france"
    fi
done