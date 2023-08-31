# pip install python-nmap
import nmap
import csv
from datetime import date
import subprocess
 

ports_from_server = ["22","80", "443", "5060", "5062", "8080"]
ports_from_windows = ["3389", "25", "445", "1433", "53", "67", "68", "161", "162", "139", "135"]


def scan_nmap_write_csv(network_range):
	today = date.today()
	save_file_from_csv = 'result_scan/csv_' + str(today) + '.csv'
	port = ', '.join(ports_from_server)
	nm = nmap.PortScanner()
	nm.scan(hosts=network_range, ports= port, arguments='-sS')  # Scan ports 80 to 443
	
	save_csv = nm.csv()
	host = nm.all_hosts()[0]
	hosts = nm.all_hosts() 
	scan_results = []
	input_data = []
	
	with open(save_file_from_csv, mode="a", newline="", encoding="utf-8") as file:
		file.write(save_csv[96::])
	'''
    print(nm.command_line())
    print(nm.scaninfo()) 
    print(save_csv)
    print( nm.all_hosts()) 
    print(nm[host].hostname()) 
    print(nm[host].state()) 
    print(nm[host].all_protocols()) 
    print(nm[host].has_tcp(22))  
'''
def scan_network(network_range):
	today = date.today()
	port = ', '.join(ports_from_windows)
	port2 = ', '.join(ports_from_server)
	write_file = 'result_scan/nmap_' + str(today) + '.txt'
	result = subprocess.run(['nmap', '-p', f'{port2}',   network_range], stdout = subprocess.PIPE, encoding='utf-8')
	
	
	with open(write_file, 'w') as f2:
		print(result.stdout, file=f2)
	print(result.stdout)
   
if __name__ == '__main__':
	network = '192.168.1.0/24'
	scan_network(network)
	
