import dbm
import json

from dataclasses import dataclass
from typing import Any, Optional

from actionpack import Action, KeyedProcedure, Procedure

from pokedex.api import Pokemon
from pokedex.api.models import PokeApiRequest
from pokedex.constants import CACHEPATH
from pokedex.db.actions import DbInsertRequestResult, DbInsertPokemon


def _persist(*pokemon: Pokemon):
    # db_inserts = (DbInsert(pk).set(name=pk['name']) for pk in pokemon)
    db_inserts = (DbInsertPokemon(pk).set(name=pk['id']) for pk in pokemon)
    procedure = KeyedProcedure(db_inserts).execute(should_raise=True)
    for key, result in procedure:
        yield key, result.value


def persist(*requests: PokeApiRequest):
# def persist(requests):
    # db_inserts = (DbInsert(pk).set(name=pk['name']) for pk in pokemon)
    # print(requests[0])
    # print(requests)
    # db_inserts = (DbInsert(key=rq.url, value=rq).set(name=rq.url) for rq in requests)

    db_inserts = (DbInsertRequestResult(key=rq.url, value=rq).set(name=rq.url) for rq in requests)
    procedure = KeyedProcedure(db_inserts).execute(should_raise=True)
    # procedure = Procedure(db_inserts).execute(should_raise=True)
    # for result in procedure:
    for key, result in procedure:
        yield key, result.value

