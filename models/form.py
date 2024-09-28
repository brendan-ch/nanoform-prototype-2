from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Form:
    title: str
    form_id: Optional[int] = None
    description: str = ''
    time_created: datetime = field(default_factory=datetime.now)