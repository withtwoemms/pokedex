from typing import Protocol, runtime_checkable

from requests import Response


@runtime_checkable
class DeferredRequest(Protocol):
    url: str

    def __call__(self) -> Response:
        classname = self.__class__.__name__
        raise NotImplementedError(
            f"Followers of the {classname} Protocol must return a {Response.__name__}"
        )
