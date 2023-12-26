import json
from dataclasses import dataclass
from typing import List, Optional
# from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel

# from pokedex.db.client import DbRead, DbInsert
from pokedex.db.actions import DbRead, DbInsert
# from pokedex.db.client import CheckKey, DbRead, DbInsert, DbInsertPokemon


# ApiResponseType = Dict[str, Any]


@dataclass(frozen=True)
class PokeApiRequest:
    url: str

    def __call__(self) -> requests.Response:
        cache_result = DbRead(self.url.encode()).perform()
        if cache_result.successful:
            response = requests.Response()
            response._content = cache_result.value
            response.status_code = 200
        else:
            response = requests.get(self.url)
            response.raise_for_status()  # TODO: handle error states
            DbInsert(
                key=self.url,
                value=json.dumps(response.json()),
            ).perform(should_raise=True)
        return response

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
