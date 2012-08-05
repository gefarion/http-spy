# Load python implementation if C implementation is not available
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


class HTTPStream:
    """
    This class represents an HTTP conversation between two hosts.
    """

    def __init__(self, tcp):
        ((self._shost, self._sport), (self._dhost, self._dport)) = tcp.addr
        server_data = tcp.server.data[:tcp.server.count]
        client_data = tcp.client.data[:tcp.client.count]
        self._server_parser = HttpParser()
        self._server_parser.execute(server_data, len(server_data))
        self._client_parser = HttpParser()
        self._client_parser.execute(client_data, len(client_data))

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
