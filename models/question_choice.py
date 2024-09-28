from dataclasses import dataclass
from typing import Optional

@dataclass
class QuestionChoice:
    choice_name: str
    choice_position: int
    choice_id: Optional[int] = None
    has_free_response_field: bool = False