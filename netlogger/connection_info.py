from dataclasses import dataclass

@dataclass(frozen=True)
class ConnectionInfo:
    remote_ip : str
    remote_port : str
    status : str
    process : str
    service : str 
    domain : str
    