# Anki rest api 

## description of the solution 
source:  csv from google translator ( saved translations )
destination: locally installed Anki application with PlugIn ankiconnect ( REST API ) use as a   

## importing from Google translator
1. https://translate.google.com/saved?sl=ru&tl=de&op=translate
2. export to Google Sheets
3. from Google Sheets: File ->download-> as csv
   ```sh
   input_file="$HOME/Downloads/Saved translations - Saved translations.csv"
   ls -la "$input_file"
   ```
4. open anki locally ( check [installation](#installation), [plugin](#anki-plugin-ankiconnect) will be activated )
   ```sh
   export ANKI_WAYLAND=1
   ./anki
   ```
5. run script
   > be aware name of your Deck should be the same as language in column 1 ( German, English ... )
   ```sh
   head "$input_file"
   
   pip3 install requests
   python3 anki-translate-uploader.py "$input_file"
   ```
6. https://translate.google.com/saved?sl=ru&tl=de&op=translate  
   UI -> right panel -> vertical 3-dots -> "clear all saved"


## anki installation 
[Anki locally installed application](https://apps.ankiweb.net/#download)
```sh
sudo snap install anki-desktop

anki-web
anki-desktop --version

# check version 
anki --version
```

## Anki plugin installation: AnkiConnect

### installation
* https://git.sr.ht/~foosoft/anki-connect
* id: 2055492159
  Anki -> ctrl+shift+a -> 2055492159
* https://ankiweb.net/shared/info/2055492159
* [github](https://github.com/FooSoft/anki-connect/tree/ankiweb?tab=readme-ov-file)
* installed folder 
```sh
cd $HOME/.local/share/Anki2/addons21/2055492159
grep -r "@util.api" -A 2 | grep 'def '
```

### read operations
⚠️ restart anki after plugin installation
```sh
curl --request POST http://127.0.0.1:8765/api/v1 \
  --header 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"decks.list","params":{}}'

## check installation 
curl localhost:8765 -X POST -d '{
    "action": "version", 
    "version": 6
}' 

## get all desks
curl localhost:8765 -X POST -d '{
    "action": "deckNames", 
    "version": 6
}' | jq .

curl localhost:8765 -X POST -d '{
    "action": "deckNamesAndIds", 
    "version": 6
}' | jq .

## get desk cards
# deck:movie*
curl -s localhost:8765 -X POST -d '{
    "action": "findCards", 
    "params": {
        "query": "deck:movie-dialog"
    },    
    "version": 6
}' | jq .

## get one card from desk by id ( previous request )
curl -s localhost:8765 -X POST -d '{
    "action": "cardsInfo", 
    "params": {
        "cards": [1760275143789]
    },    
    "version": 6
}' | jq .
```

### add card/note
```sh
## add Note
curl localhost:8765 -X POST -d '{
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": "movie-dialog",
            "modelName": "Basic",
            "fields": {
                "Front": "What is the capital of France?",
                "Back": "Paris"
            },
            "tags": ["geography"]
        }
    }
}'
```

### update card/note
```sh
curl localhost:8765 -X POST -d '{
    "action": "updateNoteFields",
    "version": 6,
    "params": {
        "note": {
            "id": 1564604895650,
            "fields": {
                "Front": "-> faith <br> She never lost faith that her missing cat would find its way home, even after months of waiting.",
                "Back": "вера"
            }
        }
    }
}'
```

# Update cards automatically
> some of the old cards have a "one-word" as a question instead of the sentence
## Steps 
1. download all the cards in the files in json format ( card_id, question, answer )
2. select only files with question less or equals two words  
   for each selected file create new file ".json.update" with addtional field ".question_sentence"
3. read all the files ".json.update" and make update via Anki REST API


### 1. Download all the cards from Anki to local folder
```sh
./walk-through-desk-save-q-a.sh

DECK_NAME=English
ls decks/$DECK_NAME
```
```json
{"card_id":1519305733793,"question":"blast","answer":"explosion, brust"}
```

### 2. walk through all the files and create 'update json' for 1-2 words 
* select only quesiton less or equals 2 words
* I want to learn english word "$question" - create one sentence with this word to depict its meaning 
```sh
export DECK_NAME=English
./walk-through-qa-extend-with-sentence.sh
```

### 3. read all the files ".json.update" and make update via Anki REST API
```sh
export DECK_NAME=English
./walk-through-update-call-restapi.sh
```