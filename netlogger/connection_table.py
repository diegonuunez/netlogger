import psutil
from .connection_raw import ConnectionRaw
from .connection_parser import ConnectionParser
from .connection_info import ConnectionInfo

class ConnectionTable:
    def __init__(self, parser: ConnectionParser):
        self.parser = parser
        self._connections: dict[tuple, ConnectionInfo] = {}
        self._new: list[ConnectionInfo] = []
        self._closed: list[ConnectionInfo] = []

    def _refresh(self) -> None:
        snapshot = {}
        for c in psutil.net_connections(kind="inet"):
            raw = ConnectionRaw.from_psutil(c)
            snapshot[self._key(raw)] = self.parser.interpret(raw)

        previous = self._connections
        self._new = [info for k, info in snapshot.items() if k not in previous]
        self._closed = [info for k, info in previous.items() if k not in snapshot]
        self._connections = snapshot

    def _all(self) -> list[ConnectionInfo]:
        return list(self._connections.values())

    def _new(self) -> list[ConnectionInfo]:
        return self._new

    def _closed(self) -> list[ConnectionInfo]:
        return self._closed

    @staticmethod
    def _key(raw: ConnectionRaw) -> tuple:
        return (raw.protocol, raw.local_connection, raw.remote_connection, raw.pid)
