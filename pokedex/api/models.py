from dataclasses import dataclass
from typing import List, Optional

import requests
from pydantic import BaseModel

from pokedex.db.client import cached_get


@dataclass(frozen=True)
class PokeApiRequest:
    url: str

    def __call__(self) -> requests.Response:
        return cached_get(self.url)

    @property
    def __name__(self):
        return f"{self.__class__.__name__}:{self.url}"


class PokeApiResourceRef(BaseModel):
    name: str
    url: str

    def as_request(self) -> PokeApiRequest:
        return PokeApiRequest(self.url)


class PokemonRef(BaseModel):
    pokemon: PokeApiResourceRef
    slot: int

    def as_api_resource_ref(self) -> PokeApiResourceRef:
        return self.pokemon

    def as_request(self) -> PokeApiRequest:
        return self.pokemon.as_request()


class PokeApiResource(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokeApiResourceRef]

    @property
    def next_request(self) -> Optional[PokeApiRequest]:
        if self.next:
            return PokeApiRequest(self.next)
