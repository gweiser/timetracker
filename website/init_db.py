import sqlite3

db = sqlite3.connect("database.db")

db.executescript(
    """
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

        DROP TABLE IF EXISTS paid;

        CREATE TABLE paid (
            id INTEGER PRIMARY KEY NOT NULL,
            creation_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            note TEXT NOT NULL,
            wage INTEGER NOT NULL,
            pay INTEGER NOT NULL
        )

        DROP TABLE IF EXISTS bin;

        CREATE TABLE bin (
            id INTEGER PRIMARY KEY NOT NULL,
            creation_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            note TEXT NOT NULL,
            wage INTEGER NOT NULL,
            pay INTEGER NOT NULL
        )        

    """
)

db.commit()
db.close()