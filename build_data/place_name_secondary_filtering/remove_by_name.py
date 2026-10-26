import re

with open("../data/dynamic/place_names_filtered_orig.csv", "r", encoding='utf-8') as r, open(
        "../data/dynamic/place_names_filtered.txt", "w", encoding='utf-8') as w:
    for line in r:
        feature_name = line.split("|", 1)[0]
        if feature_name.endswith('istrict'): continue
        if feature_name.startswith('District') and feature_name != 'District': continue
        if re.search(r'istrict [0-9ABCI]+$', feature_name): continue
        w.write(line)
