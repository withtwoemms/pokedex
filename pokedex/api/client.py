from typing import Generator, Iterable, List, Optional

import requests
from actionpack import Procedure
from actionpack.actions import Call
from actionpack.utils import Closure

from pokedex.api import PokeApiEndpoints, Pokemon
from pokedex.api.models import PokeApiResource, PokeApiResourceRef, PokemonRef
from pokedex.api.request import ApiRequest
from pokedex.api.request.protocol import DeferredRequest
from pokedex.constants import BASE_URL


ApiRequestType = ApiRequest.type()


def get_endpoints(endpoints_request: DeferredRequest) -> PokeApiEndpoints:
    response: requests.Response = endpoints_request()
    response.raise_for_status()
    endpoints: PokeApiEndpoints = response.json()
    if isinstance(endpoints, str):
        raise TypeError()
    return endpoints


def select_endpoint(name: str, endpoints: PokeApiEndpoints) -> DeferredRequest:
    return ApiRequestType(endpoints[name])


def get_resource(request: DeferredRequest) -> PokeApiResource:
    response: requests.Response = request()
    response.raise_for_status()  # TODO: handle error states
    return PokeApiResource(**response.json())


def generate_pokemon_requests(api_request: DeferredRequest, response_key: str) -> Generator[DeferredRequest, None, None]:
    response: requests.Response = api_request()
    response.raise_for_status()  # TODO: handle error states
    resource_refs = response.json()[response_key]
    for resource_ref in resource_refs:
        if response_key == "pokemon":
            model = PokemonRef(**resource_ref).as_api_resource_ref()
        else:
            model = PokeApiResourceRef(**resource_ref)
        yield model.as_request()


def get_pokemon(pokemon_requests: Iterable[DeferredRequest]) -> Generator[Pokemon, None, None]:
    calls = (Call(Closure(pokemon_request)) for pokemon_request in pokemon_requests)
    for result in Procedure(calls).execute(synchronously=False, should_raise=True):
        # TODO: consider how to proceed if `result.successful => False`
        # such handling will preclude the need for the `should_raise` option during Procedure execution
        response: requests.Response = result.value
        yield response.json()


def search_endpoint(
    endpoint_name: str, resource_ref_name: str, api_resource: Optional[PokeApiResource] = None
) -> Optional[DeferredRequest]:
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


# TODO -- consider passing an `api_request_type: type[DeferredRequest]` param.
# Doing so would give entrypoints explicit control over implementation selection at runtime.
def fetch(endpoint_name: str) -> PokeApiResource:
    endpoints = get_endpoints(ApiRequestType(BASE_URL))
    endpoint = select_endpoint(endpoint_name, endpoints)
    return get_resource(endpoint)


def get_pokemon_by_move(pokemon_move: str) -> Generator[DeferredRequest, None, None]:
    endpoint_request = search_endpoint("move", pokemon_move)
    if endpoint_request:
        yield from generate_pokemon_requests(endpoint_request, "learned_by_pokemon")


def get_pokemon_by_type(pokemon_type: str) -> Generator[DeferredRequest, None, None]:
    endpoint_request = search_endpoint("type", pokemon_type)
    if endpoint_request:
        yield from generate_pokemon_requests(endpoint_request, "pokemon")
