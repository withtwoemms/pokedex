from pathlib import Path
from typing import Dict, TypeVar
from unittest.mock import MagicMock

from actionpack.action import Result
from requests.models import Response

parentdir = Path(__file__).parent

resource_paths: Dict[str, Path] = {
    "endpoints.response": parentdir / "endpoints.response.json",
    "jigglypuff.response": parentdir / "jigglypuff.response.json",
    "pokemon.move.headbutt.response": parentdir / "pokemon.move.headbutt.response.json",
    "pokemon.moves.response.1": parentdir / "pokemon.moves.response.1.json",
    "pokemon.moves.response.2": parentdir / "pokemon.moves.response.2.json",
    "pokemon.type.fairy.response": parentdir / "pokemon.type.fairy.response.json",
    "pokemon.types.response": parentdir / "pokemon.types.response.json",
}


def resource(name: str):
    return resource_paths[name].open("rb").read()


def craft_response(contents: str, status_code: int):
    response = Response()
    response._content = contents
    response.status_code = status_code
    return response


T = TypeVar("T")


def craft_result(value: T, successful: bool) -> Result:
    mock_result = MagicMock(spec=Result)
    mock_result.successful = successful
    mock_result.value = value
    return mock_result
