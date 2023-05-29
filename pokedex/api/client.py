from typing import Any, Dict, Generator, Iterable, List, Optional, Union

import requests

from pokedex.api.constants import BASE_URL
from pokedex.api.models import PokeApiRequest, PokeApiResource, PokeApiRequest, PokeApiResourceRef, PokemonRef

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


# TODO: generalize this method
def get_pokemon_type_refs(request: PokeApiRequest) -> PokemonTypeRefs:
    response: requests.Response = request()
    response.raise_for_status()  # TODO: handle error states
    pokemon_type_resource = PokeApiResource(**response.json())
    pokemon_type_refs: List[PokeApiResourceRef] = pokemon_type_resource.results
    return pokemon_type_refs


def get_resource(request: PokeApiRequest) -> PokeApiResource:
    response: requests.Response = request()
    response.raise_for_status()  # TODO: handle error states
    return PokeApiResource(**response.json())


# TODO: generalize this
def select_pokemon_type(pokemon_type: str, pokemon_type_refs: PokemonTypeRefs) -> Optional[PokeApiRequest]:
    for pokemon_type_ref in pokemon_type_refs:
        if pokemon_type_ref.name == pokemon_type:
            return pokemon_type_ref.as_request()


def generate_pokemon_requests(api_request: PokeApiRequest, response_key: str) -> Generator[PokeApiRequest, None, None]:
    response: requests.Response = api_request()
    response.raise_for_status()  # TODO: handle error states
    resource_refs = response.json()[response_key]
    for resource_ref in resource_refs:
        if response_key == "pokemon":
            model = PokemonRef(**resource_ref).to_api_resource_ref()
        else:
            model = PokeApiResourceRef(**resource_ref)
        yield model.as_request()


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
    pokemon_requests = generate_pokemon_requests(pokemon_refs_request, "pokemon")
    yield from get_pokemon(pokemon_requests)


def search_endpoint(
    endpoint_name: str,
    resource_ref_name: str,
    api_resource: Optional[PokeApiResource] = None
) -> Optional[PokeApiRequest]:
    if not api_resource:
        api_resource = fetch(endpoint_name)

    resource_refs: List[PokeApiResourceRef] = api_resource.results
    for ref in resource_refs:
        if ref.name == resource_ref_name:
            return ref.as_request()

    if api_resource.next_request:
        response: requests.Response = api_resource.next_request()
        response.raise_for_status()  # TODO: handle error states
        new_api_resource = PokeApiResource(**response.json())
        return search_endpoint(endpoint_name, resource_ref_name, new_api_resource)


def fetch(endpoint_name: str) -> PokeApiResource:
    endpoints = get_endpoints(PokeApiRequest(BASE_URL))
    endpoint = select_endpoint(endpoint_name, endpoints)
    return get_resource(endpoint)


def get_pokemon_by_move(pokemon_move: str) -> Generator[Pokemon, None, None]:
    endpoint_request = search_endpoint("move", pokemon_move)
    if endpoint_request:
        pokemon_refs = generate_pokemon_requests(endpoint_request, "learned_by_pokemon")
        yield from get_pokemon(pokemon_refs)
