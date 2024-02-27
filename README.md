# pokedex
a tool for sourcing info about different Pokémon from the [PokéAPI](https://pokeapi.co/)


### Setup

This project uses [`poetry`](https://python-poetry.org/) as it's build tool.
It can be installed with:

```
pip install -r requirements.txt
```

This project and its dependencies can be installed with:

```
poetry install
```

Once installed, scripts can executed using the `run` subcommand.
For example, the following runs tests, coverage, and linting:

```
poetry run check
```


### Usage

There exists a `poetry` buildscript called `get-pokemon`.
It can be invoked like so:

```
poetry run get-pokemon by --type ghost
```

pipe to `less`
