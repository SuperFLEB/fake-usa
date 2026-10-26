#!/usr/bin/env python3

# Using information from FCC website searches, this finds all Kxxx/Wxxx call-signs in use
# (results/found_call_letters.txt), derives all call-signs that are not currently in use
# (results/not_found_call_letters.txt), and any call-signs that spell words at the end
# (results/<found/not_found>_<number>_letter_words.txt).
#
# Use this if you're trying to make up a fake radio or TV station, and you don't want to step on a real one,
# for instance. (Of course, check more thoroughly after the fact. Things change, and the FCC database might not be
# exhaustive.)
#
# To re-fetch all the call signs again, remove everything in the "results" directory, and it'll be retrieved and
# regenerated again.

from urllib import request
from . import states_fips
STATE_ABBREVIATION = states_fips.STATE_ABBREVIATION

WORDS_FILE = "data/static/2-3-kw4-letter-words.txt"

NOT_FOUND_FILE = "data/dynamic/call_letters_not_found.txt"
WORDS_OUTPUT_FILE = "data/dynamic/call_letters_words_not_found.txt"
KW_OUTPUT_FILE = "data/dynamic/call_letters_kw_proportion.txt"

prefixes = ("K", "W")
searchUrls = (
    "https://transition.fcc.gov/fcc-bin/amq?list=4&type=0",
    "https://transition.fcc.gov/fcc-bin/fmq?list=4&type=0",
    "https://transition.fcc.gov/fcc-bin/tvq?list=4&type=0",
)


class ThreeLetters:
    def __init__(self):
        self.kw = 0
        self.first_two = 0
        self.last = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.last += 1
        if self.last >= 27:
            self.last = 0
            self.first_two += 1

        if self.first_two >= 26 ** 2:
            raise StopIteration

        letters = tuple("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return "".join((
            letters[int(self.first_two / 26)],
            letters[self.first_two % 26],
            (letters + ('',))[self.last]
        ))


def fetch() -> dict[str, str]:
    found: dict[str, str] = {}

    for prefix in prefixes:
        for searchUrl in searchUrls:
            searchUrl = f"{searchUrl}&call={prefix}"
            with (request.urlopen(searchUrl) as res):
                print(f"Get {searchUrl}...", end="", flush=True)
                body = res.read().decode()
                print(f" Got it!")
                ABBREVIATIONS = set(STATE_ABBREVIATION.values())

                for row_text in body.split("\n"):
                    row = row_text.split("|")[1:]
                    if len(row) < 11: continue
                    callsign = row[0].strip()
                    state = row[10].strip()

                    if not callsign or not state: continue
                    if len(callsign) > 4: continue
                    if callsign[0] not in 'KW': continue
                    if state not in ABBREVIATIONS: continue
                    if callsign in found: continue

                    found[callsign] = state
    return found


def invert(found: list[str]) -> set[str]:
    all = {f"W{xxx}" for xxx in ThreeLetters()}
    all |= {f"K{xxx}" for xxx in ThreeLetters()}
    return {cs.replace(' ', '') for cs in sorted(all - set(found))}

def tag_words(callsigns: set[str]) -> set[(str, int)]:
    with open(WORDS_FILE, "r") as words_file:
        all_words = {line.strip() for line in words_file if line}
    results: set[str] = set()
    words_4 = {w for w in all_words if len(w) == 4}
    words_3 = {w for w in all_words if len(w) == 3}
    words_2 = {w for w in all_words if len(w) == 2}

    for cs in callsigns:
        if cs in words_4:
            results.add((cs, 4))
        elif cs[1:] in words_3:
            results.add((cs, 3))
        elif cs[1:3] in words_2:
            results.add((cs, 2))
        elif cs[2:] in words_2:
            results.add((cs, 2))
        else:
            results.add((cs, 0))
    return results

def main():
    stations = fetch()
    callsigns = sorted(stations.keys())
    words = tag_words(invert(callsigns))

    kw_state = {state: {"k": 0, "w": 0} for state in stations.values()}
    for cs in callsigns:
        if cs[0] == "K": kw_state[stations[cs]]["k"] += 1
        if cs[0] == "W": kw_state[stations[cs]]["w"] += 1

    with open(WORDS_OUTPUT_FILE, "w+") as words_output_file:
        words_output_file.write("callsign|word_length\n")
        words_sorted = sorted(words, key=lambda w: (-w[1], w[0]))
        words_output_file.write("\n".join([f"{w[0]}|{w[1]}" for w in words_sorted]))

    with open(KW_OUTPUT_FILE, "w+") as kw_output_file:
        kw_output_file.write("state|k1000\n")
        for state, kw_state in sorted(kw_state.items()):
            kw_proportion = int(round(kw_state['k'] / (kw_state['k'] + kw_state['w']), 3) * 1000)
            kw_output_file.write(f"{state}|{kw_proportion}\n")

if __name__ == "__main__":
    main()

