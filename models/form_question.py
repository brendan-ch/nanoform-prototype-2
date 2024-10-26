from enum import Enum
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

class FormQuestionType(Enum):
    SHORT_RESPONSE = 1
    LONG_RESPONSE = 2
    MULTIPLE_CHOICE = 3

@dataclass
class FormQuestion:
    question_type: FormQuestionType
    question_name: str
    question_position: int
    question_id: Optional[int] = None
    form_id: Optional[int] = None