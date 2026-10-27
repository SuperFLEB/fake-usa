# Fake USA

Based loosely on my prior Fake USA data compilation, this is a tool that allows you to
pick from countless plausible but fake place names by showing you names that exist, just
not in the state you selected.

It also generates fake ZIP codes and fake phone number blocks, for all your making-things-up
needs.

## Usage

### Online

The easiest way to use it is online, here at https://superfleb.github.io/fake-usa/

### At Home

It runs in the browser and works entirely offline, using a local SQLite database to fetch data.
It comes with a pre-populated database, as well as most of the tools to pull down fresh data.

```shell
git clone https://github.com/superfleb/fake-usa.git
cd fake-usa
pnpm install
pnpm dev
```

### Data-pulling scripts

It does come with a fully-populated database (`public/fakeusa.sqlite`), but if you want to pull
down fresh data, you can... mostly.

There are Python scripts to fetch the base data and populate the SQLite database, though some of the
finer details of the pre-compiled database involved more specialized and manual filtering. For the
basic set (that just has more cruft than the more polished version), run the Python scripts.

You may want to run them in a virtual environment-- doing so is an exercise left up to you, though there's
nothing terribly special about it.

```shell
cd build_data
# Go into your venv first if you have one...
pip install -r requirements.txt
python3 build_database_from_sources.py
```

The finer-polishing scripts are also in `place_name_secondary_filtering` and `sports_team_secondary_filtering`
but be advised they're a bit rough. I included them for reference, not necessarily for off-the-shelf use.

## Status and Future Plans

This is still in development. I'm cleaning up and migrating features from a prior, unpublished version,
so here's what to look out for, and what to look for in upcoming versions:

- Persistence across reloads.
- Ability to compile and save a list of generated places. More ability to tweak the generated places.
- ZIP code listings that allow you to pick "how fake" you want. Get only ZIPs that are completely unused,
  ones that are used internally by the USPS, or ones that may be valid but not for geographical addresses.
  For now, check your ZIP codes before you use them.


