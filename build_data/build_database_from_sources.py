import os

from sources.fetch_call_letters import main as fetch_call_letters_main
from sources.fetch_nanpa_npanxxx_gaps import main as fetch_nanpa_npanxxx_gaps_main
from sources.fetch_place_names import main as fetch_place_names_main
from sources.fetch_zips import main as fetch_zips_main
from sources.build_database import main as build_database_main

def wprint(wrap, text):
    print("\n" + (wrap * 80) + "\n" + text + "\n" + (wrap * 80) + "\n")

if __name__ == "__main__":
    wprint("-", "This script will fetch remote datasources and build the SQLite database.\nIt runs all of the scripts in sources/ in sequence.")
    wprint("=", "Fetch fake call letters...")
    fetch_call_letters_main()
    wprint("=", "Fetch NANPA NPA-NXX-Xnnn gaps...")
    fetch_nanpa_npanxxx_gaps_main()
    wprint("=", "Fetch place names...")
    fetch_place_names_main()
    wprint("=", "Fetch ZIP codes...")
    fetch_zips_main()
    wprint("=", "Read fetched/processed data and write SQLite database...")
    build_database_main()
