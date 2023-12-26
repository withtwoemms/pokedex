import json
import sys
from argparse import ArgumentParser

from pokedex.api.client import get_pokemon_by_move, get_pokemon_by_type
from pokedex.db.client import persist


def go(args=sys.argv):
    parser = ArgumentParser(prog="get-pokemon", description="Catch 'em all")

    subparsers = parser.add_subparsers(help="search dimension for fetching pokemon")

    parser_by = subparsers.add_parser("by")
    parser_by.add_argument("--type", type=str, help="e.g. water, grass, fire")
    parser_by.add_argument("--move", type=str, help='e.g. "water-gun", "razor-leaf", ember')

    any_args_given = len(sys.argv) > 1

    if not any_args_given:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if args.type:
        # print(json.dumps(list(get_pokemon_by_type(args.type)), indent=4))
        results = list(persist(get_pokemon_by_type(args.type)))
        report = {'persisted': dict(results), 'count': len(results)}
        print(json.dumps(report, indent=4))

    if args.move:
        move = str(args.move).replace(" ", "-")
        # print(json.dumps(list(get_pokemon_by_move(move)), indent=4))
        results = list(persist(get_pokemon_by_move(move)))
        report = {'persisted': dict(results), 'count': len(results)}
        print(json.dumps(report, indent=4))
