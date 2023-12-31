import dbm
import json
from dataclasses import dataclass
from typing import AnyStr, Optional

from actionpack import Action

from pokedex.constants import CACHEPATH
from pokedex.db.models import DeferredRequest


@dataclass
class DbInsertRequestResult(Action):
    key: AnyStr
    value: DeferredRequest
    db: Optional[str] = None

    def __post_init__(self):
        self.set(name=self.key)

    def instruction(self) -> bool:
        db = self.db or str(CACHEPATH)
        response = self.value()  # external call
        with dbm.open(db, "c") as cache:
            cache[self.key] = json.dumps(response.json())
            return True


@dataclass
class DbInsert(Action):
    key: AnyStr
    value: AnyStr
    db: Optional[str] = None

    def instruction(self) -> str:
        db = self.db or str(CACHEPATH)
        with dbm.open(db, "c") as cache:
            cache[self.key] = self.value
            return self.key


@dataclass
class DbRead(Action[str, bytes]):
    key: bytes
    db: Optional[str] = None

    def instruction(self) -> bytes:
        db = self.db or str(CACHEPATH)
        with dbm.open(db, "c") as cache:  # create db if not exists
            return cache[self.key]
