from dataclasses import dataclass

from requests import Response

from pokedex.db.client import cached_get


@dataclass(frozen=True)
class CachedPokeApiRequest:
    url: str

    def __call__(self) -> Response:
        return cached_get(self.url)

    @property
    def __name__(self):
        return f"{self.__class__.__name__}:{self.url}"
