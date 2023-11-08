import scapy.all as scapy
import nmap

def arpback(ip): # function to return MAC address of a given IP
    try:
        arp_req_frame = scapy.ARP(pdst = str(ip))
        broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
        broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame
        answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
        for i in range(0,len(answered_list)):
            return answered_list[i][1].hwsrc
    except:
        return

def osfetch(ip): # function to return the os/server of a given IP
    nm = nmap.PortScanner()
    machine = nm.scan(str(ip), arguments='-O')
    try:
        OS = machine['scan'][str(ip)]['osmatch'][0]['osclass'][0]['osfamily'].lower()
        if "linux" or "windows" in OS:
            return OS
        else:
            return "device"
    except:
        return "device"