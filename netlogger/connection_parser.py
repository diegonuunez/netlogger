import psutil
import socket
from .connection_info import ConnectionInfo
from .connection_raw import ConnectionRaw
from .dns_resolver import DNSSniffer

class ConnectionParser:
    def __init__(self):
        self._dns_cache: dict[str, str] = {}
        self._dns_sniffer = DNSSniffer()
        self._dns_sniffer.start()

    def _interpreter(self, raw: ConnectionRaw) -> ConnectionInfo:
        remote = raw.remote_connection
        ip = remote.ip if remote else ""
        port = remote.port if remote else None
        return ConnectionInfo(
            remote_ip=ip,
            remote_port=port,
            status=raw.status,
            process=self._process_name(raw.pid),
            service=self._service_for_port(port),
            domain=self._resolve_domain(ip),
        )

    def _resolve_domain(self, ip: str) -> str:
        if not ip:
            return ""
        # 1ª fuente: dominio real capturado por el sniffer DNS
        domain = self._dns_sniffer.get_domain(ip)
        if domain:
            return domain
        # fallback: reverse DNS (PTR)
        return self._reverse_dns(ip)

    def _process_name(self, pid: int) -> str:
        if pid is None:
            return ""
        try:
            return psutil.Process(pid).name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return ""

    def _service_for_port(self, port: int) -> str:
        if port is None:
            return ""
        try:
            return socket.getservbyport(port)
        except OSError:
            return ""

    def _reverse_dns(self, ip: str) -> str:
        if not ip:
            return ""
        if ip not in self._dns_cache:
            try:
                self._dns_cache[ip] = socket.gethostbyaddr(ip)[0]

            except OSError:
                self._dns_cache[ip] = ip   
        return self._dns_cache[ip]
