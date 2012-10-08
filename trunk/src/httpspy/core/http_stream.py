# Load python implementation if C implementation is not available
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

import pdb
import StringIO


class HTTPStream:
    """
    This class represents an HTTP conversation between two hosts.
    """
    @staticmethod
    def _parse_multiples_messages(data, is_response=0):
        parsers = []
        ss = StringIO.StringIO(data)
        p = HttpParser()
        s = ss.readline();
        while (s != ""):
            p.execute(s, len(s))

            if (p.is_headers_complete()):
                parsers.append(p)
                if (is_response):
                    content_length = p.get_headers().get('Content-Length')
                    if (content_length): 
                        ss.seek(int(content_length), 1) 
                    p = HttpParser() 
            s = ss.readline();

        return parsers

    @staticmethod
    def create_streams(shost, sport, sdata, dhost, dport, ddata):

        dparsers = HTTPStream._parse_multiples_messages(ddata, 0) 
        sparsers = []

        if (len(dparsers) > 0):
            sparsers = HTTPStream._parse_multiples_messages(sdata, 1)

        streams = []
        
        for i in range(0, len(sparsers)):
            streams.append(HTTPStream( 
                shost, sport, sparsers[i], 
                dhost, dport, dparsers[i]))

        return streams

    def __init__(self, shost, sport, sparser, dhost, dport, dparser):

        self._shost = shost
        self._sport = sport
        self._client_parser = sparser;

        self._dhost = dhost
        self._dport = dport
        self._server_parser = dparser;

    def get_request_headers(self):
        return self._server_parser.get_headers()

    def get_request_header(self, header):
        return self._server_parser.get_headers().get(header)

    def get_response_headers(self):
        return self._client_parser.get_headers()

    def get_response_header(self, header):
        return self._client_parser.get_headers().get(header)

    def get_url(self):
        return self._server_parser.get_url()

    def get_path(self):
        return self._server_parser.get_path()

    def get_method(self):
        return self._server_parser.get_method()

    def get_http_version(self):
        return self._server_parser.get_version()

    def get_status_code(self):
        return self._client_parser.get_status_code()

    def get_dhost(self):
        return self._dhost

    def get_dport(self):
        return self._dport

    def get_shost(self):
        return self._shost

    def get_sport(self):
        return self._sport
