CREATE TABLE Interactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOTNULL,
    english_word TEXT NOTNULL,
    current_time TEXT DEFAULT CURRENT_TIMESTAMP,
    correct BOOLEAN
);
