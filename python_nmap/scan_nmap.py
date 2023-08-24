# pip install python-nmap
import nmap


def scan_network(network_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=network_range, arguments='-p 22')  # Scan ports 22 to 443
    print(nm.command_line())
    print(nm.scaninfo())
    print(nm.csv())
    # for host in nm.all_hosts():
    #     print(f"Host: {host}")
    #     print(f"  State: {nm[host].state()}")
    #     print(f"  Ports: {nm[host]['tcp'].keys()}")



