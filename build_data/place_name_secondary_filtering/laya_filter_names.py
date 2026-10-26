from laya import Router

INPUT_PATH = "../data/dynamic/place_names.txt"
FILTERED_PATH = "../data/dynamic/place_names_filtered.txt"
REJECTED_PATH = "../data/dynamic/place_names_rejected.txt"

router = Router(device="cuda", default="english")
router.preload(["english"])

PLACE_NAME_STYLE = {
    "name_style": {
        "type": "choice",
        "instructions": (
            "Judging only from its wording, what kind of name is this? "
            "Do not decide based on whether the real feature is populated."
        ),
        "criteria": {
            "OK:simple_place_name": (
                "A standalone proper name that could plausibly be reused for a town, "
                "community, neighborhood, lake, island, or other broadly named place. "
                "Examples include Parker Lake, Bear Rapids, North Palm Beach, and Millheim."
            ),
            "OK:simple_geo_name": (
                "A proper name of a geographical feature that is just the name and type "
                "e.g., Planter Lake, South Island, Bear Rapids, Williams Pond"
            ),
            "technical_designation": (
                "A numbered, bureaucratic, electoral, governmental, infrastructural, "
                "operational, or catalog-like designation rather than an ordinary place "
                "name. Examples include District 21, Retention Pond Number 2, "
                "Commissioner District 4, and Number 3 Island."
            ),
            "dependent_subfeature": (
                "A branch, fork, prong, division, area, or other subdivision whose name "
                "depends on a larger feature or organization. Examples include North "
                "Branch, South Fork of Clear Creek, and Western Division."
            ),
            "institution_or_property": (
                "Explicitly denotes an institution, jurisdiction, reservation, club, "
                "campus, housing development, estate, or similarly site-specific property, "
                "rather than a generally reusable place name."
            ),
            "longwinded": (
                "A place name that has multiple classifying adjectives (2 or more added adjectives),"
                "especially those that are not simple prefixes like Big, Little, or compass directions."
                "Examples include Upper Blue Fish Bay, Greater Lowland Smith Lake, Outer South Barrier Island"
            )
        },
    }
}

with open(INPUT_PATH, "r", encoding="utf-8") as raw, open(FILTERED_PATH, "w", encoding="utf-8") as accepted, open(REJECTED_PATH, "w", encoding="utf-8") as rejected:
    header = raw.readline()
    accepted.write(header)
    rejected.write(header[:-1] + "|reason\n")
    for line in raw:
        placename = line.split("|")[0]
        try:
            result = router.predict(
                {"body": placename},
                PLACE_NAME_STYLE
            )
        except Exception as e:
            print("Error", e)
            continue

        choice = result["answers"]["name_style"]["choice"]
        if choice[0:2] == "OK":
            print(".", end="", flush=True)
            accepted.write(line)
        else:
            print(choice[0], end="", flush=True)
            rejected.write(line[:-1] + f"|{choice}\n")
    print("\nDone!")