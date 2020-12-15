# -*- coding: utf-8 -*-
import datetime
import logging
import os.path
import sqlite3
import string

from nmj.tables import ALL_TABLES, DbVersion, ScanDirs, ScanSystem, ShowGroups


_LOGGER = logging.getLogger(__name__)

class DBProxy(object):
	isolation_level = "DEFERRED"

	def __init__(self, root_path, popcorn_path=""):
		self.root_path = root_path
		self.popcorn_path = popcorn_path
		self.media_db_path = os.path.join(root_path, "nmj_database", "media.db")
		if not os.path.isfile(self.media_db_path):
			self.create()
		self.connection, self.cursor = self.get_connection_and_cursor()

	def get_connection_and_cursor(self):
		if not os.path.isdir(os.path.join(self.root_path, "nmj_database")):
			os.makedirs(os.path.dirname(self.media_db_path))
		connection = sqlite3.connect(self.media_db_path)
		connection.isolation_level = self.isolation_level
		connection.text_factory = str
		cursor = connection.cursor()
		return connection, cursor

	def create(self):
		_LOGGER.info("Creating database...")
		connection, cursor = self.get_connection_and_cursor()
		for table in ALL_TABLES:
			_LOGGER.debug("create table %s", table)
			table().create(cursor)
		DbVersion.insert(cursor, version="2.0.0")
		ScanDirs.insert(cursor, directory="", name=self.popcorn_path, scan_time="", size=1807172, category=3, status=3)
		ScanSystem.insert(cursor, type="RUNNING_STATUS", value="0")
		ScanSystem.insert(cursor, type="HISTORY_SCAN_VIDEOS", value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), custom1="1", custom2="89", custom3="0")
		for group in ["0-9",] + [letter for letter in string.ascii_uppercase]:
			ShowGroups.insert(cursor, name=group, language="FR")
		connection.commit()
		cursor.close()
		connection.close()
		_LOGGER.info("Database creation done")

	def contains(self, table, **kwargs):
		items = self.get_tables_items(table, **kwargs)
		return bool(items)

	def get_first(self, table, **kwargs):
		try:
			return self.get_tables_items(table, **kwargs)[0]
		except IndexError:
			return None

	def get_tables_items(self, *tables, **kwargs):
		result = []
		for table in tables:
			try:
				result += table.load(self.cursor, **kwargs)
			except:
				_LOGGER.exception("Getting items in table %s", table)
		return result

	def insert(self, table, **kwargs):
		return table.insert(self.cursor, **kwargs)

	def commit(self):
		self.connection.commit()

	def delete(self, to_remove):
		to_remove.delete(self.cursor)

	def update(self, table, item_id, **kwargs):
		item = self.get_tables_items(table, id=item_id)[0]
		item.update(self.cursor, **kwargs)
		self.commit()


