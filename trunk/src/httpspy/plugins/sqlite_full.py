from core.plugins_manager import PluginsManager 

import textwrap
import time
from datetime import datetime
import sqlite3

class SQLiteFull:

	def _create_tables(self):
		self._conn.execute('CREATE TABLE IF NOT EXISTS ' + self._table_http + 
			'''(
				id INTEGER PRIMARY KEY AUTOINCREMENT, 
				date DATE,
				shost TEXT, 
				dhost TEXT, 
				url TEXT, 
				path TEXT,
				method TEXT,
				status_code INTEGER
			)'''
		)
		self._conn.execute('CREATE TABLE IF NOT EXISTS ' + self._table_request + 
			'''(
				id INTEGER PRIMARY KEY AUTOINCREMENT, 
				http_id INTEGER,
				header TEXT,
				value TEXT
			)'''
		)
		self._conn.execute('CREATE TABLE IF NOT EXISTS ' + self._table_response + 
			'''(
				id INTEGER PRIMARY KEY AUTOINCREMENT, 
				http_id INTEGER,
				header TEXT,
				value TEXT
			)'''
		)
	
	def __init__(self, conf):
		self._dbfile = conf.get('dbfile', 'http_log.db')
		self._table_http = conf.get('table_http', 'http_info')
		self._table_request = conf.get('table_request', 'request_headers')
		self._table_response = conf.get('table_response', 'response_headers')

		self._conn = sqlite3.connect(self._dbfile)
		self._create_tables()

	def __del__(self):
		if self._conn:
			self._conn.close()

	def _log_http_info(self, http_stream):
		self._conn.execute(
			'INSERT INTO ' + self._table_http + ''' 
			(date, shost, dhost, url, path, method, status_code) 
			VALUES (?,?,?,?,?,?,?)
			''', 
			(
				datetime.now(),
				http_stream.get_shost(), 
				http_stream.get_dhost(), 
				http_stream.get_url(), 
				http_stream.get_path(), 
				http_stream.get_method(), 
				http_stream.get_status_code(), 
			)
		)

		cursor = self._conn.execute(
			"SELECT seq FROM sqlite_sequence WHERE name=?", (self._table_http,)
		)
		row = cursor.fetchone();
		return row[0]

	def _log_headers(self, table, http_id, headers): 
		self._conn.executemany(
			'INSERT INTO ' + table + ' (http_id, header, value) VALUES (?,?,?)',
			[ (http_id,) + header for header in headers.items() ]
		)

	def _log_request_headers(self, http_id, http_stream):
		self._log_headers(
			self._table_request, 
			http_id, http_stream.get_request_headers()
		)

	def _log_response_headers(self, http_id, http_stream):
		self._log_headers(
			self._table_response, 
			http_id, http_stream.get_response_headers()
		)

	def log_stream(self, http_stream):
		http_id = self._log_http_info(http_stream)
		self._log_request_headers(http_id, http_stream)
		self._log_response_headers(http_id, http_stream)
		self._conn.commit()
	
	@classmethod
	def help(cls):
		return textwrap.dedent('''\
		SQLiteFull: log data to a sqlite database
		Params:
			- dbfile            database file (default: 'http_log.db')
			- table_http        http info table (default: 'http')
			- table_request     request headers table (default: 'request_headers')
			- table_response    response_headers table (default: 'response_headers')
		''')

PluginsManager.register(SQLiteFull, 'SQLiteFull')
