import csv
import json
import requests
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python3 anki-translate-uploader.py <input_csv_file>")
    sys.exit(1)

input_file = os.path.expanduser(sys.argv[1])
anki_url = "http://localhost:8765"

def clean_text(text):
    # Remove carriage returns and non-printable ASCII, strip whitespace
    return ''.join(c for c in text if c in '\t\n\r ' or 32 <= ord(c) <= 126).strip()

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader, None)  # Skip header

    for row in reader:
        if not row or row[0] == "Deck" or not row[0].strip():
            continue

        note_deck = row[0]
        note_front = row[2] if len(row) > 2 else ""
        note_back = row[3] if len(row) > 3 else ""
        note_back_cleaned = note_back.strip()

        print(f"Deck:{note_deck}")
        print(f"Front:{note_front}")
        print(f"Back:{note_back_cleaned}\n")

        request_data = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": note_deck,
                    "modelName": "Basic",
                    "fields": {
                        "Front": note_front,
                        "Back": note_back_cleaned
                    },
                    "tags": ["googletr"]
                }
            }
        }

        response = requests.post(anki_url, json=request_data)
        print(response.json())
        print("-------------------")