# Place name secondary filtering

These are some scripts for more discretionary filtering of place names.
It's kind of a manual process, and may not be entirely necessary. In short, this is a junk pile.
If you're going to run them, they should be run in this order:

1. `lays_secondary_filtering.py` -- Uses the Laya AI to filter out some names. Takes a long time.
2. `place_name_swipe.py` -- Allows you go review any rejected names from the Laya filtering.
3. `write_filtered_place_names_database.py` -- Write the filtered/reviewed names to a database.
