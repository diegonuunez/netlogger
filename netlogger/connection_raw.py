from .connections.endpoint import Endpoint
import psutil
import socket
from dataclasses import dataclass

@dataclass(frozen=True)
class ConnectionRaw: 
    local_connection : Endpoint
    remote_connection : Endpoint
    protocol : str
    status : str
    pid : int

    @staticmethod
    def _from_psutil(c):
        return ConnectionRaw(
            local_connection = Endpoint.get_endpoint(c.laddr),
            remote_connection = Endpoint.get_endpoint(c.raddr),
            protocol = "TCP" if  c.type == socket.SOCK_STREAM else "UDP",
            status = c.status,
            pid = c.pid
        )