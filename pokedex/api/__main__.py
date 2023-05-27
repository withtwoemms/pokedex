import json
import sys
from argparse import ArgumentParser
from enum import Enum

from pokedex.api.client import get_pokemon_by_type


class Choices(Enum):
    type = "type"

    def __str__(self):
        return self.value


def go(args=sys.argv):
    parser = ArgumentParser(prog="get-pokemon", description="Catch 'em all")
    parser.add_argument("--by", type=Choices, choices=list(Choices), help="get pokemon by type")

    any_args_given = len(sys.argv) > 1

    if not any_args_given:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.by == Choices.type:
        for pokemon in get_pokemon_by_type("fairy"):
            output = json.dumps(pokemon, indent=4)
            print(output)
