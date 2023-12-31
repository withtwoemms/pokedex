from unittest import TestCase
from unittest.mock import patch

from pokedex.db.actions import DbRead
from tests.fixtures import resource


class TestActions(TestCase):
    @patch("dbm.open")
    def test_can_read_cache(self, mock_kv_open):
        key = "https://pokeapi.co/api/v2/pokemon/39/"
        pokemon_data = resource("jigglypuff.response")
        mock_kv_open.return_value.__enter__.return_value.__getitem__.return_value = pokemon_data
        mock_kv_open.assert_not_called()
        result = DbRead(key=key).perform(should_raise=True)
        mock_kv_open.assert_called_once()
        assert result.value == pokemon_data
