from unittest import TestCase
from unittest.mock import patch

import requests
from requests.exceptions import HTTPError

from pokedex.api.models import PokeApiRequest
from pokedex.db.actions import DbRead
from pokedex.db.client import cached_get, persist_requests
from tests.fixtures import craft_response, resource, craft_result


class TestClientCanCache(TestCase):
    @patch('pokedex.db.actions.DbInsertRequestResult')
    @patch.object(
        target=PokeApiRequest,
        attribute="__call__",
        side_effect=[
            craft_response(resource("jigglypuff.response"), status_code=200),
        ],
    )
    def test_can_persist_request_(self, mock_request, mock_db_insert):
        request_url = 'https://pokeapi.co/api/v2/pokemon/39/'
        mock_request.url = request_url
        key, response_data = next(persist_requests((mock_request,)))
        assert key is request_url
        assert response_data is True


class TestClientCanRetrieveFromCache(TestCase):
    @patch.object(
        target=DbRead,
        attribute="perform",
        side_effect=[
            craft_result(value=resource("jigglypuff.response"), successful=True),
        ],
    )
    def test_cache_hit(self, mock_db_reads):
        pokemon_response = cached_get('https://pokeapi.co/api/v2/pokemon/39/')
        assert pokemon_response.json()["name"] == "jigglypuff"

    @patch.object(
        target=DbRead,
        attribute="perform",
        side_effect=[
            craft_result(value=Exception('missing key.'), successful=False)
        ],
    )
    @patch.object(
        target=requests,
        attribute="get",
        side_effect=[
            craft_response('something went wrong :/', status_code=500),
        ],
    )
    def test_cache_miss_request_fail(self, mock_requests, mock_db_reads):
        with self.assertRaises(HTTPError):
            cached_get('https://pokeapi.co/api/v2/pokemon/39/')

    @patch.object(
        target=DbRead,
        attribute="perform",
        side_effect=[
            craft_result(value=Exception('missing key.'), successful=False)
        ],
    )
    @patch.object(
        target=PokeApiRequest,
        attribute="__call__",
        side_effect=[
            craft_response(resource("jigglypuff.response"), status_code=200),
        ],
    )
    def test_cache_miss_request_success(self, mock_requests, mock_db_reads):
        pokemon_response = cached_get('https://pokeapi.co/api/v2/pokemon/39/')
        assert pokemon_response.json()["name"] == "jigglypuff"
