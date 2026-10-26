import os
import sqlite3
import csv

from . import states_fips

FIPS = states_fips.FIPS
STATE_ABBREVIATION = states_fips.STATE_ABBREVIATION
STATE_NAME_DISPLAY = states_fips.STATE_NAME_DISPLAY

DB_OUTPUT_PATH = "../public/fakeusa.sqlite"


def main():
	if not os.path.isfile("data/dynamic/place_names.txt"):
		raise Exception("The file place_names.txt not found. Run fetch_place_names.py first")

	if not os.path.isfile("data/dynamic/nanpa_npanxxx_gaps.txt"):
		raise Exception("The file nanpa_npanxxx_gaps.txt not found. Run fetch_nanpa_npanxxx_gaps.py first")

	if not os.path.isfile("data/dynamic/call_letters_words_not_found.txt"):
		raise Exception("The file call_letters_words_not_found.txt not found. Run fetch_call_letters.py first")

	if os.path.exists(DB_OUTPUT_PATH) and not os.path.isfile(DB_OUTPUT_PATH):
		raise Exception(f"Database file {DB_OUTPUT_PATH} exists but is not a file.")

	os.remove(DB_OUTPUT_PATH)

	conn = sqlite3.connect(DB_OUTPUT_PATH)
	cursor = conn.cursor()

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS us_states
				   (
					   abbreviation TEXT,
					   state        TEXT,
					   fips         INTEGER PRIMARY KEY
				   )
				   ''')

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS callsigns_fake
				   (
					   callsign TEXT PRIMARY KEY,
					   word_length  INTEGER,
					   is_k         BOOLEAN
				   )
				   ''')

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS callsigns_k_proportion
				   (
					   fips  INTEGER PRIMARY KEY,
					   k1000 INTEGER -- proportion of stations in the state that start with K, x1000. For W stations, subtract from 1000.
				   )
				   ''')

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS npanxx_fake
				   (
					   npa    SMALLINT,
					   start  SMALLINT,
					   length SMALLINT,
					   fips   SMALLINT
				   )
				   ''')

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS place_names_existing
				   (
					   feature_name  TEXT,
					   fips          SMALLINT,
					   is_settlement BOOLEAN DEFAULT 0
				   )
				   ''')

	cursor.execute('''
					CREATE TABLE zip_fake (
						fips  INTEGER NOT NULL,
						zip   INTEGER NOT NULL,
						level INTEGER NOT NULL,

						PRIMARY KEY (fips, level, zip)
					) WITHOUT ROWID;
				   ''')

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS team_names
				   (
					   name TEXT PRIMARY KEY
				   )
				   ''')

	cursor.execute('''
				   CREATE TABLE IF NOT EXISTS regions
				   (
					   fips      SMALLINT,
					   region    TEXT,
					   subregion TEXT
				   )
				   ''')

	to_database = [(STATE_ABBREVIATION[fips], STATE_NAME_DISPLAY[fips], fips) for fips in STATE_ABBREVIATION.keys()]
	cursor.executemany("INSERT INTO us_states VALUES (?, ?, ?)", to_database)

	with open("data/dynamic/call_letters_words_not_found.txt", "r", encoding="utf-8") as call_letters_file:
		reader = csv.DictReader(call_letters_file, delimiter='|', quotechar='"')
		to_database = [(row['callsign'], int(row['word_length']), row['callsign'][0] == 'K') for row in reader]
		cursor.executemany("INSERT INTO callsigns_fake VALUES (?, ?, ?)", to_database)

	cursor.execute('''
				   CREATE INDEX idx_callsigns_fake_count_letters
					   ON callsigns_fake (word_length, callsign COLLATE NOCASE)
				   ''')
	cursor.execute('''
				   CREATE INDEX idx_callsigns_fake_letters_nocase
					   ON callsigns_fake (callsign COLLATE NOCASE)
				   ''')

	with open("data/dynamic/call_letters_kw_proportion.txt", "r", encoding="utf-8") as call_letters_k_file:
		reader = csv.DictReader(call_letters_k_file, delimiter='|', quotechar='"')
		to_database = [(FIPS[row['state']], int(row['k1000'])) for row in reader]
		cursor.executemany("INSERT INTO callsigns_k_proportion VALUES (?, ?)", to_database)

	with open("data/dynamic/nanpa_npanxxx_gaps.txt", "r", encoding="utf-8") as npanxx_file:
		reader = csv.DictReader(npanxx_file, delimiter='|', quotechar='"')
		to_database = [(int(row['npa']), int(row['start']), int(row['end']) - int(row['start']) + 1, FIPS[row['state']]) for row
					   in reader]
		cursor.executemany("INSERT INTO npanxx_fake VALUES (?, ?, ?, ?)", to_database)

	with open("data/dynamic/place_names.txt", "r", encoding="utf-8") as place_names_file:
		reader = csv.DictReader(place_names_file, delimiter='|', quotechar='"')
		to_database = [(row['feature_name'], int(row['fips']), row['is_settlement'] == 'TRUE') for row in
					   reader]
		cursor.executemany("INSERT INTO place_names_existing VALUES (?, ?, ?)", to_database)

	cursor.execute('''
				   CREATE INDEX idx_place_names_existing_feature_name_fips
					   ON place_names_existing (feature_name, fips)
				   ''')

	with open("data/dynamic/usable_zip_codes_by_state.txt", "r", encoding="utf-8") as place_names_file:
		reader = csv.DictReader(place_names_file, delimiter='|', quotechar='"')

		# TODO: Ingest to a flat non-block file and eliminate this block unzipping
		for block in reader:
			for zip in range(int(block['zip_start']), int(block['zip_start']) + int(block['length'])):
				to_database = [(FIPS[row['state']], row['zip_start'], row['level']) for row in reader]
				cursor.executemany("INSERT INTO zip_fake VALUES (?, ?, ?)", to_database)

	with open("data/static/team_names.txt", "r", encoding="utf-8") as team_names:
		to_database = [(line.strip(),) for line in set(team_names) if line != ""]
		cursor.executemany("INSERT INTO team_names VALUES (?)", to_database)

	with open("data/static/state_regions.csv", "r", encoding="utf-8") as state_regions_file:
		reader = csv.DictReader(state_regions_file, delimiter='|', quotechar='"')
		to_database = [(row['fips'], row['region'], row['subregion']) for row in reader]
		cursor.executemany("INSERT INTO regions VALUES (?, ?, ?)", to_database)

	cursor.execute('''
				   CREATE INDEX idx_regions_nocase
					   ON regions (fips)
				   ''')

	conn.commit()

	conn.execute("VACUUM")

	conn.close()


if __name__ == "__main__":
	main()
