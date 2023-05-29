import json
import sys
from argparse import ArgumentParser

from pokedex.api.client import get_pokemon_by_move, get_pokemon_by_type


def go(args=sys.argv):
    parser = ArgumentParser(prog="get-pokemon", description="Catch 'em all")

    subparsers = parser.add_subparsers(help="search dimension for fetching pokemon")

    parser_by = subparsers.add_parser("by")
    parser_by.add_argument("--type", type=str, help="e.g. water, grass, fire")
    parser_by.add_argument("--move", type=str, help='e.g. "water gun", "razor leaf", ember')

    any_args_given = len(sys.argv) > 1

    if not any_args_given:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.type:
        for pokemon in get_pokemon_by_type(args.type):
            output = json.dumps(pokemon, indent=4)
            print(output)

    if args.move:
        move = str(args.move).replace(" ", "-")
        for pokemon in get_pokemon_by_move(move):
            output = json.dumps(pokemon, indent=4)
            print(output)
