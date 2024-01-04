from typing import Protocol

from requests import Response


class DeferredRequest(Protocol):
    url: str

    def __call__(self) -> Response:
        classname = self.__class__.__name__
        raise NotImplementedError(
            f"Followers of the {classname} Protocol must return a {Response.__name__}"
        )
