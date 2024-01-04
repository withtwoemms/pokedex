from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class PokeApiRequest:
    url: str

    def __call__(self) -> requests.Response:
        response = requests.get(self.url)
        response.raise_for_status()
        return response

    @property
    def __name__(self):
        return f"{self.__class__.__name__}:{self.url}"
