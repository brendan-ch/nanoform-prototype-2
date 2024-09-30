from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Form:
    form_title: str
    form_id: Optional[int] = None
    form_description: str = ''