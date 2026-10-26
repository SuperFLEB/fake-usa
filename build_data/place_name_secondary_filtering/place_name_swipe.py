import readchar
from fleb.esq import ESQ

INPUT_PATH = "../data/dynamic/place_names_rejected.txt"
OUTPUT_PATH = "../data/dynamic/place_names_manual_review.txt"

header = ""

with open(INPUT_PATH, "r", encoding="utf-8") as rejected_file:
    accepted_lines: list[str] = []
    accepted: set[str] = set()
    rejected: set[str] = set()
    num_lines = sum(1 for line in rejected_file) - 1
    rejected_file.seek(0)
    header = rejected_file.readline()

    current_line = 1
    for line in rejected_file:
        line_out = line.rsplit("|", 1)[0] + "\n"
        place_name = line.split("|")[0]

        print("")
        print(f"{current_line:0>4} / {num_lines:0>4}")

        if place_name in accepted:
            print(ESQ.bright.green(f"+++ Already accepted: {place_name}"))
            accepted_lines.append(line_out)
            continue
        elif place_name in rejected:
            print(ESQ.bright.red(f"--- Already rejected: {place_name}"))
            continue

        print(ESQ.bright.red("<-- Reject | ") + ESQ.bright.cyan(f"{place_name.center(20)}") + ESQ.green(" | --> Accept:"))
        print(ESQ.dark.gray("[X] Stops and writes file, [CTRL+C] Aborts"))

        key = None
        while 1:
            key = readchar.readkey()
            if key in [readchar.key.LEFT, readchar.key.RIGHT, "X", "x"]:
                break
            print(f"Key {key} not valid. Try again.")

        if key == readchar.key.RIGHT:
            accepted.add(place_name)
            accepted_lines.append(line_out)
            print(ESQ.green(f"+++ Added: {place_name}"))
        elif key == readchar.key.LEFT:
            rejected.add(place_name)
            print(ESQ.red(f"--- Rejected: {place_name}"))
        else:
            break
        current_line += 1


with open(OUTPUT_PATH, "w", encoding="utf-8") as accepted_file:
    if len(accepted) == 0:
        print("No names kept. Nothing to write.")
    else:
        for line in accepted_lines:
            accepted_file.write(header)
            accepted_file.write(line)


