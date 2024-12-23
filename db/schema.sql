CREATE TABLE IF NOT EXISTS form (
    form_id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_title VARCHAR(64) NOT NULL,
    form_description VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS question (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id INTEGER NOT NULL,
    question_name VARCHAR(64) NOT NULL,
    question_position INTEGER NOT NULL,
    question_type INTEGER NOT NULL,

    FOREIGN KEY (form_id) REFERENCES form(form_id)
);

CREATE TABLE IF NOT EXISTS choice (
    choice_name VARCHAR(64) NOT NULL,

    choice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    choice_position INTEGER NOT NULL,
    has_free_response_field BOOLEAN NOT NULL DEFAULT FALSE,

    FOREIGN KEY (question_id) REFERENCES question(question_id)
);

CREATE TABLE IF NOT EXISTS response (
    time_submitted DATE NOT NULL,
    question_id INTEGER NOT NULL,
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,

    FOREIGN KEY (question_id) REFERENCES question(question_id)
);

CREATE TABLE IF NOT EXISTS response_choice (
    choice_id INTEGER NOT NULL,
    response_id INTEGER NOT NULL,

    -- Text associated with "Other" response, and free response text
    associated_text VARCHAR(128),

    PRIMARY KEY (response_id, choice_id)
    FOREIGN KEY (response_id) REFERENCES response(response_id)
    FOREIGN KEY (choice_id) REFERENCES choice(choice_id)
)