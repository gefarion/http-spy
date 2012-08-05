import nids
from http_stream import HTTPStream


_END_STATES = (nids.NIDS_CLOSE, nids.NIDS_TIMEOUT, nids.NIDS_RESET)


class HTTPSniffer: # Singleton Class
    """
    This class implements the actual sniffer, which reads an http conversation
    and creates an HTTPStream object based on it, and then passes it to a
    callback function.
    """

    def __init__(self):
        nids.param("scan_num_hosts", 0)  # disable portscan detection
        nids.chksum_ctl([('0.0.0.0/0', False)])  # disable checksumming

        # Default attribute values
        self._filter = ''
        self._device = ''
        self._pcapfile = ''
        self._callback = lambda x: x

    def __call__(self):
        return self

    """
    Getter & Setter methods
    """

    def get_filter(self):
        return self._filter

    def get_device(self):
        return self._device

    def get_pcapfile(self):
        return self._pcapfile

    def get_callback(self):
        return self._callback

    def set_params(self, filter=None, device=None,
                   pcapfile=None, callback=None):
        self._filter = filter or self._filter
        self._device = device or self._device
        self._pcapfile = pcapfile or self._pcapfile
        self._callback = callback or self._callback

    """
    Public methods
    """

    def start(self):
        if self._filter:
            nids.param("pcap_filter", self._filter)
        if self._pcapfile:
            nids.param("filename", self._pcapfile)
        elif self._device:
            nids.param("device", self._device)

        # Initializing libnids
        nids.init()

        # Registering the handler
        nids.register_tcp(lambda tcp: self._handle_tcp_stream(tcp))

        # Running nids
        nids.run()

    """
    Private methods
    """

    def _handle_tcp_stream(self, tcp):
        if tcp.nids_state == nids.NIDS_JUST_EST:
		((src, sport), (dst, dport)) = tcp.addr
		if dport in (80, 8000, 8080, 443, 8888):
			tcp.client.collect = 1
			tcp.server.collect = 1

        elif tcp.nids_state == nids.NIDS_DATA:
            # keep all of the stream's new data
            tcp.discard(0)

        elif tcp.nids_state in _END_STATES:
            self._callback(HTTPStream(tcp))


# Singleton class ofuscated
HTTPSniffer = HTTPSniffer()
