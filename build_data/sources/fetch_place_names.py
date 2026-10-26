from urllib import request
import tempfile
import os
import re
import zipfile
import csv

from . import states_fips
STATE_ABBREVIATION = states_fips.STATE_ABBREVIATION

NAMES_ZIP_URL = "https://prd-tnm.s3.amazonaws.com/StagedProducts/GeographicNames/DomesticNames/DomesticNames_AllStates_Text.zip"
OUTPUT_PATH = "data/dynamic/place_names.txt"


# Distinguish cities, towns, etc. from lakes and rivers, for name filtering
IS_SETTLEMENT = {
    "Bay": False,
    "Census": True,
    "Island": False,
    "Lake": False,
    "Populated Place": True,
    "Rapids": False,
    "Creek": False,
    "Civil": True
}

def is_allowed_feature(row):
    if row['feature_class'] not in (
            ["Bay", "Census", "Island", "Lake", "Populated Place", "Rapids", "Creek", "Civil"]): return False
    if row['feature_name'].count(' ') > 4: return False
    if re.search(r'^. ', row['feature_name']): return False
    if re.search(r'(North|South|East|West) Branch', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'^.+(Reservoir|Retention)', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'^.+Number [OTFSENT]', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'(University|College|Government|Branch|Fork) of', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'Metropolitan Government', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'Commissioner District', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r' Area$', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'(Lands|Villas?|Club|Prong|Band) of ', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'Estates?([- ]|$)', row['feature_name'], flags=re.IGNORECASE): return False
    if re.search(r'\d$', row['feature_name']): return False
    if re.search(r"Lake (Ten|Twenty|Thirty|Forty|Fifty|Sixty|Seventy|Eighty|Ninety|One|Two|Three|Four|Five|Six|Seven|Eight|Nine)", row['feature_name']): return False
    if re.search(r"Election", row['feature_name']): return False
    if re.search(r"Reservation^", row['feature_name']) and row['feature_name'].count(' ') > 2: return False
    if row['feature_name'].endswith("Division"): return False
    return True

def fix_name(row):
    row_name = row['feature_name']
    row_name = re.sub(r"^The ", "", row_name, flags=re.IGNORECASE)
    row_name = row_name.replace(" Census Designated Place", "")
    row_name = row_name.replace(" (historical)", "")
    row_name = row_name.replace(" Census Subarea", "")
    row_name = re.sub(r"^[^ ]+ (of|at) ", "", row_name, flags=re.IGNORECASE)
    row_name = re.sub(r"^(City|Village).+?of ", "", row_name, flags=re.IGNORECASE)
    row_name = re.sub(r"(Consolidated Borough|Unorganized Territory|Road District|Charter Township|Township) of ", "", row_name, flags=re.IGNORECASE)
    row_name = re.sub(r"^The ", "", row_name, flags=re.IGNORECASE)
    return row_name


def fetch_names_zip():
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_file_path = os.path.join(temp_dir, "names.zip")

        print(f"Downloading {NAMES_ZIP_URL} to {zip_file_path}...", flush=True, end="")
        request.urlretrieve(NAMES_ZIP_URL, zip_file_path)
        print(" Got it!")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            to_extract = [member for member in zip_ref.infolist() if
                          re.fullmatch(r"Text/DomesticNames_[A-Z]{2}\.txt", member.filename)]
            print(f"Extracting ZIP contents to {temp_dir} -- ", flush=True, end="")
            for member in to_extract:
                member.filename = member.filename.replace("Text/", "")
                zip_ref.extract(member, temp_dir)
                print(member.filename[-6:-4], flush=True, end=" ")
            print(" Done!")
            print(f"\nExtracting and writing to {OUTPUT_PATH}...")
            state_paths = [os.path.join(temp_dir, member.filename) for member in to_extract]
            with open(OUTPUT_PATH, "w+", encoding='utf-8') as output_file:
                output_file.write("feature_name|state|fips|is_settlement\n")
                for state_path in state_paths:
                    print(f"\n{state_path[-6:-4]} ", flush=True, end="")
                    tick_count = 0
                    with open(state_path, "r", newline='', encoding='utf-8') as state_file:
                        # Boolean is the IS_SETTLEMENT flag.
                        # If something is a settlement, it should be included if a non-settlement is already in the database
                        existing: dict[str, bool] = {}
                        for row in csv.DictReader(state_file, delimiter='|', quotechar='"'):
                            fips_int = int(row['state_numeric'] or "0")
                            if fips_int not in STATE_ABBREVIATION: continue
                            if not is_allowed_feature(row): continue

                            row['feature_name'] = fix_name(row)

                            verify_row = f"{row['feature_name']}|{STATE_ABBREVIATION[fips_int]}"
                            if verify_row in existing:
                                if IS_SETTLEMENT[row['feature_class']] and existing[verify_row] is False:
                                    existing[verify_row] = True
                                else:
                                    continue
                            existing[verify_row] = IS_SETTLEMENT[row['feature_class']]

                            output_file.write(f"{row['feature_name']}|{STATE_ABBREVIATION[fips_int]}|{fips_int}|{'TRUE' if IS_SETTLEMENT[row['feature_class']] else 'FALSE'}\n")
                            tick_count += 1
                            if tick_count % 50 == 0: print(f".", flush=True, end="")
                print("\nDone!")

def main():
    fetch_names_zip()


if __name__ == "__main__":
    main()
