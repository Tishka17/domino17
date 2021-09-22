from dataclasses import dataclass
from datetime import datetime


@dataclass
class UploadResult:
    path: str
    last_modified: datetime
    size: int
    key: str
    url: str
