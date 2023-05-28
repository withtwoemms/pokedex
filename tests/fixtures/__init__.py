from pathlib import Path
from typing import Dict

from requests.models import Response

parentdir = Path(__file__).parent

resource_paths: Dict[str, Path] = {
    "endpoints.response": parentdir / "endpoints.response.json",
    "jigglypuff.response": parentdir / "jigglypuff.response.json",
    "pokemon.refs.fairy.response": parentdir / "pokemon.refs.fairy.response.json",
    "pokemon.types.response": parentdir / "pokemon.types.response.json",
}


def resource(name: str):
    return resource_paths[name].open("rb").read()


def craft_response(contents: str, status_code: int):
    response = Response()
    response._content = contents
    response.status_code = status_code
    return response
