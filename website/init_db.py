import sqlite3

db = sqlite3.connect('database.db')

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
            pay INTEGER NOT NULL,
            block_id INTEGER NOT NULL,
            FOREIGN KEY(block_id) REFERENCES blocks(id)
        );

        DROP TABLE IF EXISTS blocks;

        CREATE TABLE blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );
    """
)

db.commit()
db.close()