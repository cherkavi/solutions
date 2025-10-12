# Anki rest api update
> locally installed Anki application with PlugIn ankiconnect

## importing from Google translator
1. https://translate.google.com/saved?sl=ru&tl=de&op=translate
2. export to csv/excel
3. download as csv to 
   ```sh
   input_file="$HOME/Downloads/Saved translations - Saved translations.csv"
   ls -la "$input_file"
   ```
4. "clear all saved"
5. open anki locally ( [plugin](#anki-plugin-ankiconnect) will be activated )
6. run script
   > be aware name of your Deck should be the same as language in column 1 ( German, English ... )
   ```sh
   head "$input_file"
   
   python3 anki-translate-uploader.py "$input_file"
   ```

## [Anki locally installed application](https://apps.ankiweb.net/#download)

## Anki plugin: AnkiConnect
* id: 2055492159
* https://ankiweb.net/shared/info/2055492159
* [github](https://github.com/FooSoft/anki-connect/tree/ankiweb?tab=readme-ov-file)
* installed folder 
```sh
cd $HOME/.local/share/Anki2/addons21/2055492159
grep -r "@util.api" -A 2 | grep 'def '
```

```sh
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
        "cards": [1697046994506]
    },    
    "version": 6
}' | jq .
```


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
