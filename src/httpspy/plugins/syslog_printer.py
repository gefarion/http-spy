from core.plugins_manager import PluginsManager 

import textwrap
import time
from datetime import datetime
import syslog

class SyslogPrinter:
	"""
	Esta clase toma un objeto HTTPStream y registra informacion por syslog.
	"""
	FACILITIES = {
		'LOG_KERN' 	: syslog.LOG_KERN,  
		'LOG_USER' 	: syslog.LOG_USER, 
		'LOG_MAIL' 	: syslog.LOG_MAIL, 
		'LOG_DAEMON': syslog.LOG_DAEMON, 
		'LOG_AUTH'	: syslog.LOG_AUTH, 
		'LOG_LPR'	: syslog.LOG_LPR, 
		'LOG_NEWS'	: syslog.LOG_NEWS, 
		'LOG_UUCP'	: syslog.LOG_UUCP, 
		'LOG_CRON'	: syslog.LOG_CRON, 
		'LOG_SYSLOG': syslog.LOG_SYSLOG,
		'LOG_LOCAL0': syslog.LOG_LOCAL0,
		'LOG_LOCAL1': syslog.LOG_LOCAL1,
		'LOG_LOCAL2': syslog.LOG_LOCAL2,
		'LOG_LOCAL3': syslog.LOG_LOCAL3,
		'LOG_LOCAL4': syslog.LOG_LOCAL4,
		'LOG_LOCAL5': syslog.LOG_LOCAL5,
		'LOG_LOCAL6': syslog.LOG_LOCAL6,
		'LOG_LOCAL7': syslog.LOG_LOCAL7,
	}

	PRIORITIES = {
		'LOG_EMERG'		: syslog.LOG_EMERG,
		'LOG_ALERT'		: syslog.LOG_ALERT, 
		'LOG_CRIT'		: syslog.LOG_CRIT, 
		'LOG_ERR'		: syslog.LOG_ERR, 
		'LOG_WARNING'	: syslog.LOG_WARNING, 
		'LOG_NOTICE'	: syslog.LOG_NOTICE, 
		'LOG_INFO'		: syslog.LOG_INFO, 
		'LOG_DEBUG'		: syslog.LOG_DEBUG,
	}

	def __init__(self, conf):
		self._format = conf['format'];
		facility = conf.get('facility', 'LOG_SYSLOG');
		self._facility = SyslogPrinter.FACILITIES[facility]
		priority = conf.get('priority', 'LOG_INFO');
		self._priority = SyslogPrinter.PRIORITIES[priority]
		self._undef = conf.get('undef', '')
		self._delimiter = conf.get('delimiter', ',')

		syslog.openlog(facility=self._facility)
	
	def _parse_http_stream(self, http_stream):
		http_data = {}
		http_data['url'] = http_stream.get_url()
		http_data['path'] = http_stream.get_path()
		http_data['method'] = http_stream.get_method()
		http_data['dhost'] = http_stream.get_dhost()
		http_data['dport'] = http_stream.get_dport()
		http_data['sport'] = http_stream.get_sport()
		http_data['shost'] = http_stream.get_shost()
		http_data['http_version'] =  ".".join(map(str, http_stream.get_http_version()))
		http_data['status_code'] = http_stream.get_status_code()

		date = datetime.now()
		http_data['ctime'] = date.ctime()
		http_data['timestamp'] = int(time.mktime(date.timetuple()))

		request_headers = http_stream.get_request_headers()
		for header in request_headers:
			http_data['>' + header] = request_headers.get(header)

		response_headers = http_stream.get_response_headers()
		for header in response_headers:
			http_data['<' + header] = response_headers.get(header)

		return http_data

	def log_stream(self, http_stream):
		http_data = self._parse_http_stream(http_stream)
		query_data = [ key + '=' + str(http_data.get(key, self._undef)) for key in self._format.split() ]	
		syslog.syslog(self._priority, self._delimiter.join(query_data))

	@classmethod
	def help(cls):
		return textwrap.dedent('''\
		SyslogPrinter: Log request information using syslog 
		Params:
			- format           string made from keys separated by spaces
			- undef (opt)      string to use in undefined headers (default: '')
			- delimiter (opt)  format keys separator (default: ',')
			- priority (opt)   priority level for syslog, see 'man syslog' (default: LOG_INFO)
			- facility (opt)   facility for syslog, see 'man syslog' (default: LOG_SYSLOG)
		Keys: 
			- Request: url, path, method, http_version, 
			- Response: status_code
			- Hosts: dhost, dport, shost, sport
			- Request headers: >User-Agent, >Host, >Accept, > + 'header name'
			- Response headers: <Content-Type, <Server, < + 'header name'
			- Other: ctime, timestamp
		Example:
			- format: 'shost >Host path <Content-Type'
		''')

PluginsManager.register(SyslogPrinter, 'SyslogPrinter')
