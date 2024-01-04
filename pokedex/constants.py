from pathlib import Path
from os import environ


PROJECTROOT = Path(__file__).parent.parent.absolute()
DBROOT = PROJECTROOT / "pokedex" / "db"
CACHEPATH = DBROOT / "cache"

BASE_URL = "https://pokeapi.co/api/v2/"

API_REQUEST_IMPL = environ.get("API_REQUEST_IMPL") or "DEFAULT"
