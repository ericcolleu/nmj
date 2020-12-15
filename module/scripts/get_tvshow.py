#!/usr/bin/python
from nmj.db.constants import SEASON_TITLE_TYPE
from nmj.tables import Shows
from nmj.updater import NMJUpdater
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.getLogger("nmj.updater").setLevel(logging.DEBUG)
updater = NMJUpdater(sys.argv[1])
serie_id=updater.get_show_id_from_title("Esprits Criminels")
tvshow=updater.db.get_first(Shows)
for season in updater.db.get_tables_items(Shows, ttid=tvshow.ttid, title_type=SEASON_TITLE_TYPE):
    print(season)
nmj_show = updater.get_show(updater.get_show_id_from_title("Esprits Criminels"))
print(nmj_show)
details = nmj_show.jsondetails()
print(len(details["seasons"][0]["episodes"]))
print(len(details["seasons"][1]["episodes"]))
