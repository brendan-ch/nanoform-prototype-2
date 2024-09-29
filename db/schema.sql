CREATE TABLE IF NOT EXISTS form (
    form_id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_title VARCHAR(64) NOT NULL,
    form_description VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS question (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_id INTEGER NOT NULL,
    question_title VARCHAR(64) NOT NULL,
    question_type INTEGER NOT NULL,

    FOREIGN KEY (form_id) REFERENCES form(form_id)
);

CREATE TABLE IF NOT EXISTS choice (
    choice_title VARCHAR(64) NOT NULL,

    -- ID is static regardless of position within question
    -- But is unique within the associated question only
    choice_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    choice_position INTEGER UNIQUE NOT NULL,

    PRIMARY KEY (choice_id, question_id)
    FOREIGN KEY (question_id) REFERENCES question(question_id)
);

CREATE TABLE IF NOT EXISTS response (
    time_submitted DATE NOT NULL,
    question_id INTEGER NOT NULL,

    selected_choice INTEGER,
    -- Text associated with "Other" response, and free response text
    associated_text VARCHAR(128),

    response_id INTEGER PRIMARY KEY AUTOINCREMENT,

    FOREIGN KEY (question_id) REFERENCES question(question_id)
    FOREIGN KEY (selected_choice) REFERENCES choice(choice_id)
);

