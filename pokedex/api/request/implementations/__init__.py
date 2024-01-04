from enum import Enum

from pokedex.api.request.implementations.default import PokeApiRequest
from pokedex.api.request.implementations.cached import CachedPokeApiRequest
from pokedex.api.request.protocol import DeferredRequest


class ApiRequest(Enum):
    DEFAULT: DeferredRequest = PokeApiRequest
    CACHED: DeferredRequest = CachedPokeApiRequest

    @property
    def type(self):
        return self.value
