from xlsx2csv import Xlsx2csv
from urllib import request
import re

from . import states_fips
STATE_NAME_TO_ABBR = states_fips.STATE_NAME_TO_ABBR

ZIP_TYPE_USED = 3
ZIP_TYPE_UNIQUE = 2
ZIP_TYPE_POBOX = 1
ZIP_TYPE_UNUSED = 0

ZIP_LOCALE_DETAIL_LANDING_URL = 'https://postalpro.usps.com/ZIP_Locale_Detail'
ZIP_LOCALE_DETAIL_KNOWN_URL = 'https://postalpro.usps.com/mnt/glusterfs/2026-09/ZIP_Locale_Detail.xlsx'

# The USPS XLSF file is garbage-- the column headings are across multiple rows and there are a bunch of spaces.
# You might need to change these if the format changes.
ZIP_LOCALE_DETAIL_OFFSET_COLUMN_NAMES = {
    "Detail": 0,
    "Unique": 2,
    "Other": 2,
}

def fetch_locale_detail():
    print("Fetching USPS ZIP Locale Detail Landing Page... ", flush=True, end="")
    with request.urlopen(ZIP_LOCALE_DETAIL_LANDING_URL) as response:
        html_content = response.read().decode('utf-8')
        print("Got it!")

        match = re.search(r'data-src="(https://postalpro.usps.com/[^"]+/ZIP_Locale_Detail.xlsx)"', html_content)
        xlsx_url = ZIP_LOCALE_DETAIL_KNOWN_URL

        if match:
            xlsx_url = match.group(1)
            print(f"Latest ZIP Locale Detail XSLF file URL: {xlsx_url}")

        print("Downloading ZIP Locale Detail XSLF file...", flush=True, end="")
        request.urlretrieve(xlsx_url, 'data/dynamic/USPS_ZIP_Locale_Detail.xlsx')
        print("Got it!")

        print("Converting XSLF to CSVs: ", flush=True, end="")
        with Xlsx2csv('data/dynamic/USPS_ZIP_Locale_Detail.xlsx', delimiter="|") as xlsx_file:
            xlsx_file.convert('data/dynamic/USPS_ZIP_Locale_Detail_Detail.csv', sheetname='Detail')
            print("Detail", flush=True, end="")
            xlsx_file.convert('data/dynamic/USPS_ZIP_Locale_Detail_Unique.csv', sheetname='Unique')
            print(", Unique", flush=True, end="")
            xlsx_file.convert('data/dynamic/USPS_ZIP_Locale_Detail_Other.csv', sheetname='Other')
            print(", Other", flush=True)

def compile_positive_lists():
    zips: dict[int, tuple[str, set[str]]] = {}
    for subset, offset in ZIP_LOCALE_DETAIL_OFFSET_COLUMN_NAMES.items():
        print(f"Compiling positive list for {subset}...", flush=True)
        with open(f"data/dynamic/USPS_ZIP_Locale_Detail_{subset}.csv", "r", encoding="utf-8") as csv_file:
            line_number = -1
            for line in csv_file:
                line_number += 1
                # Skip all header rows (hence the <=)
                if line_number <= offset: continue
                cols = line.split("|")

                zipcode = int(cols[3])
                z_class = cols[4].strip()
                district = cols[1].strip()
                p_state = cols[10].strip()
                zip_detail = zips.get(zipcode, (z_class, set()))

                # District is...
                #    multiple state abbreviations -- "MA-RI"
                #    multiple state abbreviations and numbers -- "MA-RI 2"
                #    a single state name -- "NEW YORK"
                # or a state name and number(s) -- "MICHIGAN 2"
                if "-" in district:
                    for state in district.split("-"):
                        zip_detail[1].add(state[:2].upper())
                else:
                    state_name = re.sub(r" \d+$", "", district)
                    if state_name in STATE_NAME_TO_ABBR:
                        zip_detail[1].add(STATE_NAME_TO_ABBR[state_name])

                # Include the "physical state name"
                zip_detail[1].add(p_state)

                zips[zipcode] = zip_detail

    return zips

# TODO:
# Since we're not using runs in the database any more, this might be obsolete. We can probably factor this out
# to make a flat (non-run) file, and change build_database.py to just cycle through a flat file.
def find_usable_zip_runs(zip_details: dict[int, tuple[str, set[str]]]):
    print("Filter and compile unused ZIP codes...", flush=True, end="")

    # [(start, length, zip_type, {state,...})]
    # Initialize with "00000" being "used" because it's not a valid ZIP code
    runs: list[tuple[int, int, int, set[str]]] = ([(0, 1, ZIP_TYPE_USED, set())])
    sorted_zip_details: list[tuple[int, str, set[str]]] = [(zd[0], zd[1][0], zd[1][1]) for zd in sorted(zip_details.items())]

    for (zip_code, zip_type, states) in sorted_zip_details:
        normalized_zip_type = {"P": ZIP_TYPE_POBOX, "U": ZIP_TYPE_UNIQUE}.get(zip_type, ZIP_TYPE_USED)
        current_run = runs[-1]
        run_next_zip = current_run[0] + current_run[1]

        if zip_code == run_next_zip and normalized_zip_type == current_run[2] and states == current_run[3]:
            # This can continue the run
            runs[-1] = (current_run[0], current_run[1] + 1, current_run[2], current_run[3])
            continue

        # Make or extend a nonexistent run if there is a gap between this run and the last one
        if zip_code > run_next_zip:
            # Make a new run of unused, with this and prior run's states
            runs.append((run_next_zip, zip_code - run_next_zip, ZIP_TYPE_UNUSED, states | runs[-1][3]))

        # Make a new run
        run = (zip_code, 1, normalized_zip_type, states)
        runs.append(run)

    # Make a run for the last ZIP code
    if runs[-1][0] + runs[-1][1] < 100000:
        run_next_zip = runs[-1][0] + runs[-1][1]
        runs.append((run_next_zip, 100000 - run_next_zip, ZIP_TYPE_UNUSED, runs[-1][3]))

    # Filter out used runs
    print("Done!", flush=True)
    return [run for run in runs if run[2] != ZIP_TYPE_USED]

def write_usable_zips(usable_zip_runs: list[tuple[int, int, int, set[str]]]):
    print("Write output: Expand multi-state runs...", flush=True, end="")

    # Unzip multi-state runs
    usable_zip_runs_by_state: dict[str, list[tuple[str, int, int, int]]] = {}
    for run in usable_zip_runs:
        for state in run[3]:
            if state not in usable_zip_runs_by_state:
                usable_zip_runs_by_state[state] = []
            usable_zip_runs_by_state[state].append((state, run[0], run[1], run[2]))

    print("Done! Write output file...", flush=True, end="")

    with open("data/dynamic/usable_zip_codes_by_state.txt", "w", encoding="utf-8") as csv_file:
        csv_file.write("state|zip_start|length|level")
        for state in sorted(usable_zip_runs_by_state.items()):
            for run in sorted(state[1]):
                csv_file.write(f"\n{run[0]}|{run[1]}|{run[2]}|{run[3]}")
    print("Done!")

def main():
    fetch_locale_detail()
    zips = compile_positive_lists()
    usable = find_usable_zip_runs(zips)
    write_usable_zips(usable)

if __name__ == "__main__":
    main()