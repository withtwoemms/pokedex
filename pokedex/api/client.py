from typing import Any, Dict, Generator, Iterable, List, Optional, Union

import requests

from pokedex.api.constants import BASE_URL
from pokedex.api.models import PokeApiRequest, PokeApiResource, PokeApiResourceRef, PokemonRef

PokeApiEndpoints = Dict[str, str]
PokemonTypeRefs = List[PokeApiResourceRef]
PokemonTypes = Dict[str, Union[Optional[str], List[Dict[str, str]]]]
Pokemon = Dict[str, Any]


def get_endpoints(endpoints_request: PokeApiRequest) -> PokeApiEndpoints:
    response: requests.Response = endpoints_request()
    response.raise_for_status()  # TODO: handle error states
    endpoints: PokeApiEndpoints = response.json()
    return endpoints


def select_endpoint(name: str, endpoints: PokeApiEndpoints) -> PokeApiRequest:
    return PokeApiRequest(endpoints[name])


def get_pokemon_type_refs(request: PokeApiRequest) -> PokemonTypeRefs:
    response: requests.Response = request()
    response.raise_for_status()  # TODO: handle error states
    pokemon_type_resource = PokeApiResource(**response.json())
    pokemon_type_refs: List[PokeApiResourceRef] = pokemon_type_resource.results
    return pokemon_type_refs


def select_pokemon_type(pokemon_type: str, pokemon_type_refs: PokemonTypeRefs) -> Optional[PokeApiRequest]:
    for pokemon_type_ref in pokemon_type_refs:
        if pokemon_type_ref.name == pokemon_type:
            return pokemon_type_ref.as_request()


def get_pokemon_refs(pokemon_type_request: PokeApiRequest) -> Generator[PokemonRef, None, None]:
    response: requests.Response = pokemon_type_request()
    response.raise_for_status()  # TODO: handle error states
    pokemon_refs = response.json()["pokemon"]
    for pokemon_ref in pokemon_refs:
        yield PokemonRef(**pokemon_ref).as_request()


# TODO: make concurrent
def get_pokemon(pokemon_requests: Iterable[PokeApiRequest]) -> Generator[Pokemon, None, None]:
    for pokemon_request in pokemon_requests:
        response: requests.Response = pokemon_request()
        response.raise_for_status()  # TODO: handle error states
        yield response.json()


def get_pokemon_by_type(pokemon_type: str):
    endpoints = get_endpoints(PokeApiRequest(BASE_URL))
    endpoint = select_endpoint("type", endpoints)
    pokemon_type_refs = get_pokemon_type_refs(endpoint)
    pokemon_refs_request = select_pokemon_type(pokemon_type, pokemon_type_refs)
    pokemon_refs = get_pokemon_refs(pokemon_refs_request)
    yield from get_pokemon(pokemon_refs)


def get_pokemon_by_move(pokemon_move: str) -> Generator[Pokemon, None, None]:
    raise NotImplementedError
