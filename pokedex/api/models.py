from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
import requests


ApiResponseType = Dict[str, Any]


@dataclass(frozen=True)
class PokeApiRequest:
    url: str

    def __call__(self) -> ApiResponseType:
        return requests.get(self.url)


class PokeApiResourceRef(BaseModel):
    name: str
    url: str

    def as_request(self) -> PokeApiRequest:
        return PokeApiRequest(self.url)


class PokemonRef(BaseModel):
    pokemon: PokeApiResourceRef
    slot: int

    def as_request(self) -> PokeApiRequest:
        return self.pokemon.as_request()


class PokeApiResource(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokeApiResourceRef]
