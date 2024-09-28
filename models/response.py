from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Response:
    selected_choice_id: int
    question_id: int
    associated_text: Optional[str] = None
    response_id: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)