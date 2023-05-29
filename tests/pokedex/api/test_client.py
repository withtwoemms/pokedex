from types import GeneratorType
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import HTTPError

from pokedex.api.client import get_pokemon_by_move, get_pokemon_by_type
from pokedex.api.models import PokeApiRequest
from tests.fixtures import craft_response, resource


class TestClientCanGetPokemonByType(TestCase):
    @patch.object(
        PokeApiRequest,
        "__call__",
        side_effect=[
            craft_response(resource("endpoints.response"), status_code=200),
            craft_response(resource("pokemon.types.response"), status_code=200),
            craft_response(resource("pokemon.type.fairy.response"), status_code=200),
            craft_response(resource("jigglypuff.response"), status_code=200),
        ],
    )
    def test_entrypoint_happy_path(self, mock_requests):
        fairies = get_pokemon_by_type("fairy")
        assert isinstance(fairies, GeneratorType)

        pokemon = next(fairies)
        assert pokemon["name"] == "jigglypuff"

    @patch.object(
        PokeApiRequest,
        "__call__",
        side_effect=[
            craft_response(resource("endpoints.response"), status_code=500),
            craft_response(resource("pokemon.types.response"), status_code=200),
            craft_response(resource("pokemon.type.fairy.response"), status_code=200),
            craft_response(resource("jigglypuff.response"), status_code=200),
        ],
    )
    def test_entrypoint_initial_api_call_failure(self, mock_requests):
        with self.assertRaises(HTTPError):
            next(get_pokemon_by_type("fairy"))


class TestClientCanGetPokemonByMove(TestCase):
    @patch.object(
        PokeApiRequest,
        "__call__",
        side_effect=[
            craft_response(resource("endpoints.response"), status_code=200),
            craft_response(resource("pokemon.moves.response.1"), status_code=200),
            craft_response(resource("pokemon.moves.response.2"), status_code=200),
            craft_response(resource("pokemon.move.headbutt.response"), status_code=200),
            craft_response(resource("jigglypuff.response"), status_code=200),
        ],
    )
    def test_entrypoint_happy_path(self, mock_requests):
        pounders = get_pokemon_by_move("headbutt")
        assert isinstance(pounders, GeneratorType)

        pokemon = next(pounders)
        assert pokemon["name"] == "jigglypuff"

    @patch.object(
        PokeApiRequest,
        "__call__",
        side_effect=[
            craft_response(resource("endpoints.response"), status_code=500),
            craft_response(resource("pokemon.moves.response.1"), status_code=200),
            craft_response(resource("pokemon.moves.response.2"), status_code=200),
            craft_response(resource("pokemon.move.headbutt.response"), status_code=200),
            craft_response(resource("jigglypuff.response"), status_code=200),
        ],
    )
    def test_entrypoint_initial_api_call_failure(self, mock_requests):
        with self.assertRaises(HTTPError):
            next(get_pokemon_by_move("double-slap"))
