# pokedex
a tool for sourcing info about different Pokémon from the [PokéAPI](https://pokeapi.co/)


### Overview

API requests are to the Pokedex API using the console script entrypoint.
The console script leverages functions within the `pokedex.client` module.
This module relies agnostically on the contents of the `pokedex.api.request` package:
```
pokedex/api/request/
├── __init__.py
├── implementations
│   ├── __init__.py  <-- Implementation bindings here!
│   ├── cached.py
│   ├── default.py
│   └── ...
└── protocol.py
```
Therein, a protocol is defined.
This protocol definition serves as the structural "template" for how different types of requests can be implemented.
Implementations have their own module (for clarity) and are "registered" for use outside of the package by the `ApiRequest` enum.
Environment variables can be used with the console script entrypoint to bind an implementation at runtime(see ["Usage" section](#usage)).
When new implementations have been deployed, choice of implmentation is made as simple as changing the environment.

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
