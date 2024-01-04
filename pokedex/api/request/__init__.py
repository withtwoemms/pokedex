from enum import Enum
from typing import Type

from pokedex.api.request.implementations.cached import CachedPokeApiRequest
from pokedex.api.request.implementations.default import PokeApiRequest
from pokedex.api.request.protocol import DeferredRequest
from pokedex.constants import API_REQUEST_IMPL


class ApiRequest(Enum):
    DEFAULT: DeferredRequest = PokeApiRequest
    CACHED: DeferredRequest = CachedPokeApiRequest

    @staticmethod
    def type() -> Type[DeferredRequest]:
        return ApiRequest[API_REQUEST_IMPL].value
