#!/usr/bin/python
import logging
import optparse
import os
import pprint
import time

from nmj.updater import NMJEditor


_LOGGER = logging.getLogger("nmj")
def get_lock(root_dir):
	while os.path.isfile(os.path.join(root_dir, "pynmj.lock")):
		time.sleep(0.5)
	fd = file(os.path.join(root_dir, "pynmj.lock"), "w+")
	fd.write("lock\n")
	fd.close()

def release_lock(root_dir):
	os.remove(os.path.join(root_dir, "pynmj.lock"))

def parse_options():
	parser = optparse.OptionParser()

	parser.add_option(
		"-n", "--clean-name",
		dest="clean_name", action="store_true", default=False,
		help="Clean videos file names",
	)
	return parser.parse_args()

logging.basicConfig(level=logging.DEBUG)
#_LOGGER.setLevel(logging.INFO)
options, arguments = parse_options()
get_lock(arguments[0])
try:
	editor = NMJEditor(arguments[0], "local_directory")
	for result in editor.search(arguments[1]):
		print("%s" % str(result).encode("ascii", "replace"))
finally:
	release_lock(arguments[0])


