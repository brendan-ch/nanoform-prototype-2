from dataclasses import dataclass
from models.form import Form
from models.form_question_with_choices import FormQuestionWithChoices

@dataclass
class FormWithQuestions(Form):
    questions: list[FormQuestionWithChoices]