from typing import List, Optional

from pydantic import BaseModel

from pokedex.api.request import ApiRequest
from pokedex.api.request.protocol import DeferredRequest


class PokeApiResourceRef(BaseModel):
    name: str
    url: str

    def as_request(self) -> DeferredRequest:
        return ApiRequest.type()(self.url)


class PokemonRef(BaseModel):
    pokemon: PokeApiResourceRef
    slot: int

    def as_api_resource_ref(self) -> PokeApiResourceRef:
        return self.pokemon

    def as_request(self) -> DeferredRequest:
        return self.pokemon.as_request()


class PokeApiResource(BaseModel):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PokeApiResourceRef]

    @property
    def next_request(self) -> Optional[DeferredRequest]:
        if self.next:
            return ApiRequest.type()(self.next)
