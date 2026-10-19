#!/usr/bin/env python3
"""Build cards/fixtures/base_set_cards.json from the Pokémon TCG API.

Run once, on a developer's machine, then commit the fixture:

    python scripts/build_base_set_fixture.py
    python manage.py loaddata base_set_cards

The live site never calls the API. It only reads its own database, so
there is no API key to protect and no outside service it depends on.
The API works without a key for a one-off run like this; if one is
set in the POKEMONTCG_API_KEY environment variable it is sent too.

Card data and images: Pokémon TCG API, https://pokemontcg.io
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "cards" / "fixtures" / "base_set_cards.json"

SET_ID = "base1"
SET_SIZE = 102
URL = "https://api.pokemontcg.io/v2/cards"
# The API often answers with a server error (HTTP 5xx), more so for
# large pages, so fetch 25 cards a page and retry each page patiently.
PAGE_SIZE = 25
ATTEMPTS = 10

# The Base Set is CardSet 1 (pokemon_cardsets.json). Cards 1 to 3 are
# the AAA, BBB and CCC tester cards, so Base Set card N gets pk 3 + N.
BASE_SET_PK = 1
PK_OFFSET = 3

RARITIES = {
    "Common": "COMMON",
    "Uncommon": "UNCOMMON",
    "Rare": "RARE",
    "Rare Holo": "RARE_HOLO",
}


def fetch_page(page, headers):
    """Download one page of the set, retrying if the API has a hiccup."""
    query = f"?q=set.id:{SET_ID}&pageSize={PAGE_SIZE}&page={page}"
    request = urllib.request.Request(URL + query, headers=headers)
    for attempt in range(1, ATTEMPTS + 1):
        try:
            # Always the fixed https:// address in URL above.
            opened = urllib.request.urlopen(request, timeout=60)  # nosec
            with opened as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code < 500 or attempt == ATTEMPTS:
                raise
            print(f"Page {page}: HTTP {error.code}, retrying...")
            time.sleep(min(3 * attempt, 15))


def fetch_cards():
    """Download every card in the set as a list of dictionaries."""
    headers = {"User-Agent": "CardVault fixture builder"}
    api_key = os.environ.get("POKEMONTCG_API_KEY")
    if api_key:
        headers["X-Api-Key"] = api_key
    cards, page = [], 1
    while True:
        result = fetch_page(page, headers)
        cards += result["data"]
        if len(cards) >= result["totalCount"] or not result["data"]:
            return cards
        page += 1


def to_fixture(cards):
    """Check the API's data and turn it into Django fixture objects."""
    numbers = sorted(int(card["number"]) for card in cards)
    if numbers != list(range(1, SET_SIZE + 1)):
        sys.exit(f"Expected cards 1 to {SET_SIZE}, got {len(numbers)}.")
    fixture = []
    for card in sorted(cards, key=lambda card: int(card["number"])):
        rarity = card.get("rarity")
        # The API gives basic Energy cards no rarity; the printed Base
        # Set marks them Common.
        if rarity is None and card.get("supertype") == "Energy":
            rarity = "Common"
        if rarity not in RARITIES:
            sys.exit(f"Unknown rarity {rarity!r} on {card['name']}.")
        number = int(card["number"])
        fields = {
            "name": card["name"],
            "card_set": BASE_SET_PK,
            "number": number,
            "rarity": RARITIES[rarity],
            "image_url": card["images"]["small"],
        }
        fixture.append({
            "model": "cards.card",
            "pk": PK_OFFSET + number,
            "fields": fields,
        })
    return fixture


def main():
    fixture = to_fixture(fetch_cards())
    text = json.dumps(fixture, indent=2, ensure_ascii=False)
    OUTPUT.write_text(text + "\n", encoding="utf-8")
    print(f"Wrote {len(fixture)} cards to {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
