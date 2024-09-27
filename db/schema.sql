CREATE TABLE IF NOT EXISTS form (
    form_id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_title VARCHAR(64) NOT NULL,
    form_description VARCHAR(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS question (
    question_id INTEGER NOT NULL PRIMARY KEY,
    form_id INTEGER NOT NULL,
    question_title VARCHAR(64) NOT NULL,

    FOREIGN KEY (form_id) REFERENCES form(form_id)
);

CREATE TABLE IF NOT EXISTS choice (
    choice_title VARCHAR(64) NOT NULL,
    choice_position INTEGER NOT NULL
    question_id INTEGER NOT NULL,

    FOREIGN KEY (question_id) REFERENCES question(question_id)
);

