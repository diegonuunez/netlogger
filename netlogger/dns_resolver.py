from scapy.all import sniff
from scapy.layers.dns import DNS
import threading 


class DNSSniffer:
    def __init__(self):
        self._domain_dict = {}

    def _process_pkt(self,pkt) -> None:
        if pkt.haslayer(DNS) and pkt[DNS].qr == 1:
            dns = pkt[DNS]
            domain = dns.qd.qname.decode().rstrip(".")       
            for i in range(dns.ancount):
                rr = dns.an[i]
                if rr.type == 1:                       
                    self._domain_dict[rr.rdata] = domain

    def get_domain(self, ip: str) -> str:
        return self._domain_dict.get(ip, "")

    def start(self):
        # daemon=True => el hilo muere solo cuando acaba el programa
        thead = threading.Thread(
            target=lambda: sniff(filter="udp port 53", prn=self._process_pkt, store=False),
            daemon=True,
        )
        thead.start()