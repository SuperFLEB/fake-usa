from fleb.esq import ESQ
from laya import Router

INPUT_PATH = "../data/static/team_names.txt"
FILTERED_PATH = "../data/static/team_names_filtered.txt"

router = Router(device="cuda", default="english")
router.preload(["english"])

TEAM_NAME_RULES = {
    "normal": {
        "type": "noul",
        "instructions": (
            "Is this a good name for an American sports team?"
        )
    },
    "mascot": {
        "type": "noul",
        "instructions": (
            "Is this name an animal, profession, or broad archetype that would make a good character for a sports team mascot?"
        )
    },
    "general": {
        "type": "noul",
        "instructions": (
            "Is this name specific to a location, in that it refers to local lore or customs and not a general character or concept?"
        )
    },
    "offense": {
        "type": "noul",
        "instructions": "Does this text or string contain explicit racial slurs, derogatory ethnic slurs, or hate speech symbols?"
    },
    "political": {
        "type": "noul",
        "instructions": "Does this text or string contain references to political parties, movements, or organizations?"
    },
    "ethnic": {
        "type": "noul",
        "instructions": "Does this text or string contain references to ethnic groups, cultures, or nationalities, EXCEPT general references to Americans?"
    }
}

with open(INPUT_PATH, "r", encoding="utf-8") as raw, open(FILTERED_PATH, "w", encoding="utf-8") as accepted:
    for line in raw:
        team_name = line.strip()
        try:
            result = router.predict(
                {"body": team_name},
                TEAM_NAME_RULES
            )
        except Exception as e:
            print("Error", e)
            continue

        match_n = result["answers"]["normal"]["noul"]
        match_g = result["answers"]["general"]["noul"]
        match_m = result["answers"]["mascot"]["noul"]
        match_o = result["answers"]["offense"]["noul"]
        match_p = result["answers"]["political"]["noul"]
        match_e = result["answers"]["ethnic"]["noul"]

        if (match_n > 0.3 or match_m > 0.6):
            if match_g > 0.7:
                print(ESQ.red("[ Specific ] " + team_name) + ESQ.dark.gray(f" Nrm: {match_n:.2f} Mas: {match_m:.2f} Gen: {match_g:.2f}"))
                continue
            if match_o > 0.8 or match_p > 0.8 or match_e > 0.9:
                print(ESQ.red("[ OPE      ] " + team_name) + ESQ.dark.gray(f" Off: {match_o:.2f} Pol: {match_p:.2f} Eth: {match_e:.2f}"))
                continue
            print(ESQ.green("[ Accepted ] " + team_name) + ESQ.dark.gray(f" Nrm: {match_n:.2f} Mas: {match_m:.2f} Gen: {match_g:.2f}"))
            accepted.write(line)
        else:
            print(ESQ.red("[ Weak     ] " + team_name) + ESQ.dark.gray(f" Nrm: {match_n:.2f} Mas: {match_m:.2f} Gen: {match_g:.2f}"))

    print("\nDone!")
