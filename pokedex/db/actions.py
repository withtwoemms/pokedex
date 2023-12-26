import dbm
import json
from dataclasses import dataclass
from typing import Optional

from actionpack import Action

from pokedex.api import Pokemon
from pokedex.api.models import PokeApiRequest
from pokedex.constants import CACHEPATH


@dataclass
class DbInsertPokemon(Action[str, str]):
    pokemon: Pokemon

    def instruction(self, db: Optional[str] = None) -> bool:
        db = db or CACHEPATH
        with dbm.open(db, 'c') as cache:  # create db if not exists
            cache[self.name] = json.dumps(self.pokemon, indent=4)  # consider alternative serialization
            return self.pokemon['name']


@dataclass
class DbInsertRequestResult(Action):
    key: str
    value: PokeApiRequest
    # value: Any  # PokeApiRequest

    def instruction(self, db: Optional[str] = None) -> str:
        db = db or CACHEPATH
        outcome = self.value().json()
        with dbm.open(db, 'c') as cache:
            # cache[self.key] = self.value()
            cache[self.key] = json.dumps(outcome, indent=4)
            return self.key


@dataclass
class DbInsert(Action):
    key: str
    value: str

    def instruction(self, db: Optional[str] = None) -> str:
        db = db or CACHEPATH
        with dbm.open(db, 'c') as cache:
            cache[self.key] = self.value
            return self.key


@dataclass
class DbRead(Action[str, bytes]):
    key: bytes

    def instruction(self, db: Optional[str] = None) -> bytes:
        db = db or CACHEPATH
        with dbm.open(db, 'c') as cache:  # create db if not exists
            return cache[self.key]


@dataclass
class CheckKey(Action[str, bool]):
    key: bytes

    def instruction(self, db: Optional[str] = None) -> bool:
        db = db or CACHEPATH
        with dbm.open(db, 'c') as cache:  # create db if not exists
            return self.key in cache


# class DB:
    

# @dataclass
# class DbInsert:
#     pokemon: Pokemon

#     def __call__(self, db: Optional[str] = None) -> Call:
#         return Call(Closure[bool](self.execute, db=db))
        
#     def execute(self, db: Optional[str] = None):
#         db = db or 'cache'
#         with dbm.open(db, 'c') as cache:  # create db if not exists
#             key = self.pokemon['name']
#             cache[key] = json.dumps(self.pokemon, indent=4)  # consider alternative serialization
#         return True




# @dataclass
# class DbInserts:
#     pokemon: Iterable[Pokemon]

#     def __call__(self, db: Optional[str] = None) -> bool:
