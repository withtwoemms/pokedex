import dbm
import json
from dataclasses import dataclass
from typing import AnyStr, Optional

from actionpack import Action

from pokedex.api import Pokemon
from pokedex.constants import CACHEPATH
from pokedex.db.models import DeferredRequest


@dataclass
class DbInsertPokemon(Action):
    pokemon: Pokemon

    def instruction(self, db: Optional[str] = None) -> bool:
        db = db or str(CACHEPATH)
        with dbm.open(db, 'c') as cache:  # create db if not exists
            cache[self.name] = json.dumps(self.pokemon, indent=4)  # consider alternative serialization
            return self.pokemon['name']


@dataclass
class DbInsertRequestResult(Action):
    key: AnyStr
    value: DeferredRequest

    def __post_init__(self):
        self.set(name=self.key)

    def instruction(self, db: Optional[str] = None) -> bool:
        db = db or str(CACHEPATH)
        response = self.value()
        with dbm.open(db, 'c') as cache:
            cache[self.key] = json.dumps(response.json())
            return True


@dataclass
class DbInsert(Action):
    key: AnyStr
    value: AnyStr

    def instruction(self, db: Optional[str] = None) -> str:
        db = db or str(CACHEPATH)
        with dbm.open(db, 'c') as cache:
            cache[self.key] = self.value
            return self.key


@dataclass
class DbRead(Action[str, bytes]):
    key: bytes

    def instruction(self, db: Optional[str] = None) -> bytes:
        db = db or str(CACHEPATH)
        with dbm.open(db, 'c') as cache:  # create db if not exists
            return cache[self.key]
