from types import GeneratorType
from unittest import TestCase

from pokedex.api.client import get_pokemon_by_type

from pokedex.api.models import PokeApiRequest
from tests.fixtures import craft_response, resource
from unittest.mock import patch


class TestClient(TestCase):

    @patch.object(PokeApiRequest, '__call__', side_effect=[
            craft_response(resource('endpoints.response'), status_code=200),
            craft_response(resource('pokemon.types.response'), status_code=200),
            craft_response(resource('pokemon.refs.fairy.response'), status_code=200),
            craft_response(resource('jigglypuff.response'), status_code=200),
        ]
    )
    def test_get_pokemon_by_type(self, mock_requests):
        fairies = get_pokemon_by_type('fairy')
        assert isinstance(fairies, GeneratorType)

        pokemon = next(fairies)
        assert pokemon['name'] == 'jigglypuff'
