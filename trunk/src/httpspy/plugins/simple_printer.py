from core.plugins_manager import PluginsManager

import textwrap
import time
from datetime import datetime


class SimplePrinter:
    """
    Esta clase toma un objeto HTTPStream y registra informacion por pantalla.
    """

    def __init__(self, conf):
        self._format = conf['format']
        self._delimiter = conf.get('delimiter', ' ')
        self._undef = conf.get('undef', '-')

    def _parse_http_stream(self, http_stream):
        http_data = {}
        http_data['url'] = http_stream.get_url()
        http_data['path'] = http_stream.get_path()
        http_data['method'] = http_stream.get_method()
        http_data['dhost'] = http_stream.get_dhost()
        http_data['dport'] = http_stream.get_dport()
        http_data['sport'] = http_stream.get_sport()
        http_data['shost'] = http_stream.get_shost()
        http_data['http_version'] = ".".join(map(str, http_stream.get_http_version()))
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
        query_data = [str(http_data.get(key, self._undef))
        for key in self._format.split()]
        print self._delimiter.join(query_data)

    @classmethod
    def help(cls):
        return textwrap.dedent('''\
SimplePrinter: print to stdout the especified information
Params:
- format           string made from keys separated by spaces
- undef (opt)      string to use in undefined headers (default: '-')
- delimiter (opt)  string delimiter for the keys (default: ' ')
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


# Registering the plugin in the plugin manager
PluginsManager.register(SimplePrinter, 'SimplePrinter')
