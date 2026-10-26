import os
import sqlite3
import csv

DB_OUTPUT_PATH = "../../public/fakeusa.sqlite"

def main():
    conn = sqlite3.connect(DB_OUTPUT_PATH)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM team_names')

    with open("../data/static/team_names.txt", "r", encoding="utf-8") as team_names:
        to_database = [(line.strip(),) for line in set(team_names) if line != ""]
        cursor.executemany("INSERT INTO team_names VALUES (?)", to_database)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
