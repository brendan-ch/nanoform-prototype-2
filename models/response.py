from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Response:
    question_id: int
    selected_choice_ids: int | list[int] = field(default_factory=lambda: [])
    associated_text: Optional[str] = None
    response_id: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)