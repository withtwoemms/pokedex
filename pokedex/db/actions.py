import dbm
import json
from dataclasses import dataclass
from typing import AnyStr, Optional

from actionpack import Action

from pokedex.api.request.protocol import DeferredRequest
from pokedex.constants import CACHEPATH


@dataclass
class DbInsertRequestResult(Action):
    key: AnyStr
    value: DeferredRequest
    db: Optional[str] = None
    metadata: bool = True

    def __post_init__(self):
        self.set(name=self.key)

    def instruction(self) -> bool:
        db = self.db or str(CACHEPATH)
        response = self.value()  # external call
        with dbm.open(db, "c") as cache:
            record = response.json()
            cache[self.key] = json.dumps(record)
            return True if self.metadata else record


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
