import json
import sys
from argparse import ArgumentParser

from pokedex.api.client import get_pokemon_by_type


def go(args=sys.argv):
    parser = ArgumentParser(prog="get-pokemon", description="Catch 'em all")
    parser.add_argument("--by", choices=["type"], help="get pokemon by type")

    any_args_given = len(sys.argv) > 1

    if not any_args_given:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    if args.by:
        result = list(get_pokemon_by_type("fairy"))
        output = json.dumps(result, indent=4)
        print(output)
