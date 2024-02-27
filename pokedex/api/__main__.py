import click

from pokedex.api.client import get_pokemon_by_move, get_pokemon_by_type
from pokedex.db.client import persist_requests
from pokedex.db.models import Report


@click.group()
def cli():
    pass


@cli.command(no_args_is_help=True)
@click.option("--type", type=click.STRING, default=False, help="e.g. water, grass, fire")
@click.option("--move", type=click.STRING, default=False, help="e.g. water-gun, razor-leaf, ember")
def by(type: str, move: str):
    """
    Accepts values by which to fetch Pokemon

    TODO: dismiss mutual exclusivity for given options--
    i.e. `--type` and `--move` should be usable at the same time
    """
    if type != "False":
        results = dict(persist_requests(get_pokemon_by_type(type)))
        print(Report(persisted=results))
        return

    if move != "False":
        results = dict(persist_requests(get_pokemon_by_move(move)))
        print(Report(persisted=results))
        return


def go():
    return cli()
