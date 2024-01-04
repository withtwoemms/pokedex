import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Type, Union

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]


@dataclass
class Report:
    persisted: dict

    def __str__(self) -> JSON:
        summary = dict(asdict(self), count=len(self.persisted))
        return json.dumps(summary, indent=4)
