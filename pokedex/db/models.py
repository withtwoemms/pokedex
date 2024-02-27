import json
from dataclasses import asdict, dataclass


@dataclass
class Report:
    persisted: dict

    def __str__(self) -> str:
        summary = dict(asdict(self), count=len(self.persisted))
        return json.dumps(summary, indent=4)
