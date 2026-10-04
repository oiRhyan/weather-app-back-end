import sqlite3

for database in ["data/database/atlas.db", "data/database/inmet.db"]:
    connection = sqlite3.connect(database)

    print(f"\n===== {database} =====")

    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    for (table,) in tables:
        print(f"\n--- {table} ---")

        columns = connection.execute(
            f'PRAGMA table_info("{table}")'
        ).fetchall()

        for column in columns:
            print(column)

    connection.close()