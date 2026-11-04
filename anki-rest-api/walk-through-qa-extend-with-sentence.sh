for file in decks/"$DECK_NAME"/*.json; do
  # Extract filename, question, and answer separated by tabs
  IFS=$'\t' read -r fname card_id question answer < <(
    jq -r --arg fn "$(basename "$file")" '
      select((.question // "" | split(" ") | length) <= 2) | 
      [$fn, (.card_id // "" | tostring), .question, .answer] | @tsv
    ' "$file"
  )

  # If question is not empty (meaning it matched the condition)
  if [ -n "$question" ]; then
    echo "---------"
    echo "File:     $fname"
    echo "Question: $question"
    echo "Answer:   $answer"
    destination_file="decks/${DECK_NAME}/"$(basename "$file")".update"

    if [ ! -e $destination_file ]; then   # re-run possibility         
        request="For english word $question - create one sentence with this word to depict its meaning. Output ONLY the pure answer via stdin. Exclude all wrappers, formatting, and commentary"
        # request="I want to learn english word $question - create one sentence with this word to depict its meaning. Generate MP3 file with this sentence $fname.mp3 . Output ONLY the pure answer to the input text provided via stdin. Exclude all wrappers, formatting, and commentary"
        
        # generated_sentence=$(opencode run "$request")
        generated_sentence=$(copilot -p "$request" --silent)
        if [ -z "$generated_sentence" ]; then
            break
        fi

        echo "$card_id" 
        echo "$question" 
        echo "$generated_sentence" 
        echo "$answer" 

        jq -n \
        --argjson card_id "$card_id" \
        --arg q "$question" \
        --arg x "$generated_sentence" \
        --arg a "$answer" \
        '{card_id: $card_id, question: $q, question_sentence: $x, answer: $a}' > "$destination_file"
        sleep 2
        echo "------------------------"
    fi
  fi
done
