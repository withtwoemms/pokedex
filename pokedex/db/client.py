import json
from typing import Iterable

import requests
from actionpack import KeyedProcedure

from pokedex.db.actions import DbInsert, DbInsertRequestResult, DbRead
from pokedex.db.models import DeferredRequest


def persist_requests(requests: Iterable[DeferredRequest]):
    db_inserts = (DbInsertRequestResult(key=rq.url, value=rq) for rq in requests)
    procedure = KeyedProcedure[str, dict](db_inserts).execute(should_raise=True)
    for key, result in procedure:
        yield key, result.value


def cached_get(url: str) -> requests.Response:
    cache_result = DbRead(url.encode()).perform()
    if cache_result.successful:
        response = requests.Response()
        response._content = cache_result.value
        response.status_code = 200
    else:
        response = requests.get(url)
        response.raise_for_status()  # TODO: handle error states
        DbInsert(key=url, value=json.dumps(response.json())).perform(should_raise=True)
    return response
