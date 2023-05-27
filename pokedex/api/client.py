from typing import Any, Dict, Generator, Iterable, List, Optional, Union

from pokedex.api.models import PokeApiRequest, PokeApiResourceRef, PokemonRef


PokeApiEndpoints = Dict[str, str]
PokemonTypeRefs = List[PokeApiResourceRef] 
PokemonTypes = Dict[str, Union[Optional[str], List[Dict[str, str]]]]
Pokemon = Dict[str, Any]


def get_endpoints(endpoints_request: PokeApiRequest) -> PokeApiEndpoints:
    raise NotImplementedError


def get_pokemon_type_refs(request: PokeApiRequest) -> PokemonTypeRefs:
    raise NotImplementedError


def get_pokemon_refs(pokemon_type_request: PokeApiRequest) -> Generator[PokemonRef, None, None]:
    raise NotImplementedError


def get_pokemon(pokemon_requests: Iterable[PokeApiRequest]) -> Generator[Pokemon, None, None]:
    raise NotImplementedError
    

def get_pokemon_by_type(pokemon_type: str):
    raise NotImplementedError
