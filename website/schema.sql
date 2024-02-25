DROP TABLE IF EXISTS entries;

CREATE TABLE entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    duration INTEGER NOT NULL,
    note TEXT NOT NULL,
    wage INTEGER NOT NULL,
    pay INTEGER NOT NULL
);