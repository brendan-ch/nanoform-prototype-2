from dataclasses import dataclass, field
from models.form import Form
from models.form_question_with_choices import FormQuestionWithChoices
from typing import Optional

@dataclass
class FormWithQuestions(Form):
    questions: Optional[list[FormQuestionWithChoices]] = None