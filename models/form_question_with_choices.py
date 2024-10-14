from dataclasses import dataclass, field
from models.question_choice import QuestionChoice
from models.form_question import FormQuestion

@dataclass
class FormQuestionWithChoices(FormQuestion):
    choices: list[QuestionChoice] = field(default_factory=[])