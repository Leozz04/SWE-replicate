from __future__ import annotations

from simple_parsing.helpers.serialization.serializable import FrozenSerializable
from pathlib2 import Path
from dataclasses import dataclass
@dataclass(frozen=True)
class Command(FrozenSerializable):
    code: str
    name: str
    docstring: str | None = None
    end_name: str | None = None  # if there is an end_name, then it is a multi-line command
    arguments: dict | None = None
    signature: str | None = None