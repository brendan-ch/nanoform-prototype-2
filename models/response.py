from datetime import datetime

class Response:
    def __init__(
        self,
        selected_choice_id: int,
        question_id: int,
        associated_text = None,
        timestamp = datetime.now(),
        response_id = None  # optional for responses not yet in database
    ):
        self.selected_choice_id = selected_choice_id
        self.question_id = question_id
        self.timestamp = timestamp
        self.associated_text = associated_text
        self.response_id = response_id
