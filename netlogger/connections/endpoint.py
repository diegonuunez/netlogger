import psutil
from dataclasses import dataclass

@dataclass(frozen=True)
class Endpoint: 
    ip : str
    port : int 

    def _get_endpoint(addr):
        if not addr:
            return None
        return Endpoint(addr.ip, addr.port)
