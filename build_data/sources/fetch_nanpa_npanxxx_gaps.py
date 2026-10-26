from urllib import request
import tempfile
import os
import zipfile
import csv

THOUSANDS = (
    "https://reports.nanpa.com/public/ThousandsBlockAssignment_All_Augmented.zip",
    "ThousandsBlockAssignment_All_Augmented.zip",
    "ThousandsBlockAssignment_All_Augmented.txt"
)

CO_CODE_ASSIGNMENT = (
    "https://reports.nanpa.com/public/CoCodeAssignment_Utilized_AllStates_Public.zip",
    "CO_Code_Assignment.zip",
    "CoCodeAssignment_Utilized_AllStates_Public.txt"
)

OUTPUT_PATH = "data/dynamic/nanpa_npanxxx_gaps.txt"


_NXXX_TEMPLATE = {nxxx for nxxx in range(2000, 10000) if
               nxxx // 10 % 100 != 11 and  # No N11 numbers
               nxxx // 10 not in (555, 958, 959)
               }
def generate_nxxx_set() -> set[int]:
    return _NXXX_TEMPLATE.copy()

def get_gaps(csv_file, non_pooled: set[tuple[int, int]]) -> list[tuple[int, int, int, str]]:
    reader = csv.DictReader(csv_file, delimiter=',')
    free_npanxxx: dict[int, tuple[set[int], str]] = dict()

    # Scan the thousands block assignment file and eliminate anything found there
    # prev_npa isn't necessary, but it should speed things up by only looking in the set when the NPA changes
    prev_npa = None
    for row in reader:
        npa = int(row['NPA'])
        nxxx = int(row['NXX'] + row['X'])
        if npa != prev_npa:
            prev_npa = npa
            if npa not in free_npanxxx:
                free_npanxxx[npa] = (generate_nxxx_set(), row['State'])
        npaxxx_set = free_npanxxx[npa][0]

        if row['STATUS'] != 'AV':
            npaxxx_set.discard(nxxx)

    for npa, nxx in non_pooled:
        for nxxx in range(nxx * 10, (nxx + 1) * 10):
            if npa in free_npanxxx:
                free_npanxxx[npa][0].discard(nxxx)

    # Condense the results
    condensed_gaps: list[tuple[int, int, int, str]] = []
    for npa, contents in free_npanxxx.items():
        blocks = sorted(contents[0])
        start_nxxx = prev_nxxx = blocks.pop(0)
        for nxxx in blocks:
            if prev_nxxx == nxxx - 1:
                prev_nxxx = nxxx
                continue
            condensed_gaps.append((npa, start_nxxx * 1000, (prev_nxxx + 1) * 1000 - 1, contents[1]))
            start_nxxx = prev_nxxx = nxxx
    return condensed_gaps

def get_non_pooled(columnar_file):
    non_pooled: set[tuple[int, int]] = set()
    headings = next(columnar_file)
    npanxx_offset = headings.index('NPA-NXX')
    pc_offset = headings.index('Pooled Code')

    for row in columnar_file:
        npanxx = row[npanxx_offset:npanxx_offset+7]
        pc = row[pc_offset]
        if pc == 'N':
            non_pooled.add(tuple(map(int, npanxx.split('-'))))
    return non_pooled

def fetch_zip():
    with tempfile.TemporaryDirectory() as temp_dir:
        co_zip_path = os.path.join(temp_dir, "CO_Code_Assignment.zip")

        for url, filename, member in [CO_CODE_ASSIGNMENT, THOUSANDS]:
            zip_path = os.path.join(temp_dir, filename)
            print(f"Downloading {url} to {zip_path}...", flush=True, end="")
            request.urlretrieve(url, zip_path)
            print(" Got it!")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extract(member, temp_dir)
                print("Extracted it!")

        with open(os.path.join(temp_dir, CO_CODE_ASSIGNMENT[2]), 'r') as csv_file:
            non_pooled = get_non_pooled(csv_file)
            print(f"Ignoring {len(non_pooled)} non-pooled exchanges.")

        with open(os.path.join(temp_dir, THOUSANDS[2]), 'r') as csv_file:
             gaps = get_gaps(csv_file, non_pooled)

        with open(OUTPUT_PATH, "w+") as output_file:
            output_file.write("npa|start|end|state\n")
            for npa, fromnxxx, tonxxx, state in sorted(gaps):
                output_file.write(f"{npa}|{fromnxxx}|{tonxxx}|{state}\n")

def main():
    fetch_zip()

if __name__ == "__main__":
    main()
