from core.plugins_manager import PluginsManager 

import textwrap
import time
from datetime import datetime
import MySQLdb

class MySQLFull: 
	
	def _create_tables(self):
		cursor = self._db.cursor()

		cursor.execute('CREATE TABLE IF NOT EXISTS ' + self._table_http + 
			'''(
				id INTEGER PRIMARY KEY AUTO_INCREMENT, 
				date DATETIME,
				shost TEXT, 
				dhost TEXT, 
				url TEXT, 
				path TEXT,
				method TEXT,
				status_code SMALLINT
			)'''
		)

		cursor.execute('CREATE TABLE IF NOT EXISTS ' + self._table_request + 
			'''(
				id INTEGER PRIMARY KEY AUTO_INCREMENT, 
				http_id INTEGER,
				header TEXT,
				value TEXT
			)'''
		)
		cursor.execute('CREATE TABLE IF NOT EXISTS ' + self._table_response + 
			'''(
				id INTEGER PRIMARY KEY AUTO_INCREMENT, 
				http_id INTEGER,
				header TEXT,
				value TEXT
			)'''
		)
	
	def __init__(self, conf):

		self._table_http = conf.get('table_http', 'http_info')
		self._table_request = conf.get('table_request', 'request_headers')
		self._table_response = conf.get('table_response', 'response_headers')

		host=conf.get('host', 'localhost')
		port=conf.get('port', '3306')
		user=conf.get('user', 'root')
		passwd=conf.get('passwd', '')
		db=conf.get('database', 'httpspy')

		self._db = MySQLdb.connect(
			host=host, port=int(port), user=user, passwd=passwd, db=db)

		self._create_tables()

	def __del__(self):
		if self._db:
			self._db.close()

	def _log_http_info(self, http_stream):
		cursor = self._db.cursor()
		cursor.execute(
			'INSERT INTO ' + self._table_http + ''' 
			(date, shost, dhost, url, path, method, status_code) 
			VALUES (NOW(),%s,%s,%s,%s,%s,%s)
			''', 
			(
				http_stream.get_shost(), 
				http_stream.get_dhost(), 
				http_stream.get_url(), 
				http_stream.get_path(), 
				http_stream.get_method(), 
				http_stream.get_status_code()
			)
		)

		cursor.execute("SELECT LAST_INSERT_ID()")
		row = cursor.fetchone();

		return row[0]

	def _log_headers(self, table, http_id, headers): 
		cursor = self._db.cursor()
		cursor.executemany(
			'INSERT INTO ' + table + ' (http_id, header, value) VALUES (%s,%s,%s)',
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
	
	@classmethod
	def help(cls):
		return textwrap.dedent('''\
		MySQLFull: log data to a mysql data base
		Params:
			- host              mysql database host (default: 'localhost')
			- port              mysql database port (default: '3306')
			- user              mysql database user (default: 'root')
			- passwd            mysql database user passwd (default: '')
			- database          database for the tables (default: 'httpspy')
			- table_http        http info table (default: 'http')
			- table_request     request headers table (default: 'request_headers')
			- table_response    response_headers table (default: 'response_headers')
		''')

PluginsManager.register(MySQLFull, 'MySQLFull')
