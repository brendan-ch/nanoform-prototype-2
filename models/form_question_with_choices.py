from dataclasses import dataclass, field
from models.question_choice import QuestionChoice
from models.form_question import FormQuestion
from typing import Optional

@dataclass
class FormQuestionWithChoices(FormQuestion):
    choices: Optional[list[QuestionChoice]] = None