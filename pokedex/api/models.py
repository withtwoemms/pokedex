from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel

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

    def to_api_resource_ref(self) -> PokeApiRequest:
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
