from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Response:
    question_id: int
    response_id: Optional[int] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ResponseChoice:
    choice_id: int
    response_id: int
    associated_text: Optional[str] = None
