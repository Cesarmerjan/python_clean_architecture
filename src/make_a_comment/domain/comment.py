import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(unsafe_hash=True)
class Comment:
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    text: str = field(default="", hash=False)
    datetime: "datetime" = field(
        default_factory=datetime.now, hash=False,  init=False)
