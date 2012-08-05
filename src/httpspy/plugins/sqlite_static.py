from core.plugins_manager import PluginsManager 

import textwrap
import time
from datetime import datetime
import sqlite3

class SQLiteStatic:

	def __init__(self, conf):
		self._dbfile = conf.get('dbfile', 'http_log.db')
		self._table = conf.get('table', 'http_log')
		self._conn = sqlite3.connect(self._dbfile)
		self._conn.execute('CREATE TABLE IF NOT EXISTS ' + self._table + 
			'''(
				id INTEGER PRIMARY KEY AUTOINCREMENT, 
				date DATE,
				shost TEXT, 
				host TEXT, 
				path TEXT,
				method TEXT,
				status_code INTEGER,
				content_type TEXT,
				content_length INTEGER
			)'''
		)

	def __del__(self):
		if self._conn:
			self._conn.close()
	
	def log_stream(self, http_stream):
		self._conn.execute(
			'INSERT INTO ' + self._table + ''' 
			(date, shost, host, path, method, status_code, 
			content_type, content_length) 
			VALUES (?,?,?,?,?,?,?,?)
			''', 
			(
				datetime.now(),
				http_stream.get_shost(), 
				http_stream.get_request_header('Host'),
				http_stream.get_path(), 
				http_stream.get_method(), 
				http_stream.get_status_code(), 
				http_stream.get_response_header('Content-Type'),
				http_stream.get_response_header('Content-Length'),
			)
		)
		self._conn.commit()
	
	@classmethod
	def help(cls):
		return textwrap.dedent('''\
		SQLiteStatic: log data to a sqlite database
		Params:
			- dbfile            database file (default: 'http_log.db')
			- table             table target (default: 'http_log')
		Data stored:
			- id                id key (INTEGER) 
			- date              date of request (DATE)
			- shost             source host (TEXT)
			- host              destination host (TEXT)
			- path              request path (TEXT)
			- method            request method (TEXT)
			- status_code       response status code (INTEGER)
			- content_type      response content type (TEXT)
			- content_length    response length (INTEGER)
		''')

PluginsManager.register(SQLiteStatic, 'SQLiteStatic')
