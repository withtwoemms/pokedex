import json
from unittest import TestCase

from pokedex.db.models import Report


class TestReport(TestCase):

    def test_report_representation(self):
        results = {
            "https://pokeapi.co/api/v2/pokemon/1/": True,
            "https://pokeapi.co/api/v2/pokemon/2/": True,
            "https://pokeapi.co/api/v2/pokemon/3/": False,
        }
        report = Report(persisted=results)
        expected_report = json.dumps(
            {"persisted": results, "count": len(results)},
            indent=4
        )

        assert str(report) == expected_report
