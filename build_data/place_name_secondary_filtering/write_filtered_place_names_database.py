import os
import sqlite3
import csv

DB_OUTPUT_PATH = "../../public/fakeusa.sqlite"

def main():
    conn = sqlite3.connect(DB_OUTPUT_PATH)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS place_names_existing
                   (
                       feature_name  TEXT,
                       state         TEXT,
                       fips          SMALLINT,
                       is_settlement BOOLEAN DEFAULT 0
                   )
                   ''')

    cursor.execute('DELETE FROM place_names_existing')

    with open("../data/dynamic/place_names_filtered.txt", "r", encoding="utf-8") as place_names_filtered_file:
        reader = csv.DictReader(place_names_filtered_file, delimiter='|', quotechar='"')
        to_database = [(row['feature_name'], row['state'], int(row['fips']), row['is_settlement'] == 'TRUE') for row in
                       reader]
        cursor.executemany("INSERT INTO place_names_existing VALUES (?, ?, ?, ?)", to_database)


    try:
        with open("../data/dynamic/place_names_revived.txt", "r", encoding="utf-8") as place_names_revived_file:
            reader = csv.DictReader(place_names_revived_file, delimiter='|', quotechar='"')
            to_database = [(row['feature_name'], row['state'], int(row['fips']), row['is_settlement'] == 'TRUE') for row in
                           reader]
            cursor.executemany("INSERT INTO place_names_existing VALUES (?, ?, ?, ?)", to_database)
    except FileNotFoundError:
        print("No revived place names file found.")
        pass

    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
