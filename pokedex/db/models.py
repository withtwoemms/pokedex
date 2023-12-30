import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Type, Union

from requests import Response
from typing_extensions import Protocol


class DeferredRequest(Protocol):
    url: str

    def __call__(self) -> Response:
        pass


JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


@dataclass
class Report:
    persisted: dict

    def __str__(self) -> JSON:
        summary = dict(asdict(self), count=len(self.persisted))
        return json.dumps(summary, indent=4)
