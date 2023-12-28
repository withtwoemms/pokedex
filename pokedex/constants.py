from pathlib import Path


PROJECTROOT = Path(__file__).parent.parent.absolute()
DBROOT = PROJECTROOT / 'pokedex' / 'db'
CACHEPATH = DBROOT / 'cache'
