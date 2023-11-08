# pip install python-nmap
import nmap
import csv
from datetime import datetime
import subprocess
from static.py.python_nmap.exam_fping import fping_all


today = datetime.now()
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
	port = ', '.join(ports_from_windows)
	port2 = ', '.join(ports_from_server)
	write_file = 'result_scan/nmap_' + str(today) + '.txt'
	result = subprocess.run(['nmap', '-p', f'{port2}',   network_range], stdout = subprocess.PIPE, encoding='utf-8')
	with open(write_file, 'w') as f2:
		print(result.stdout, file=f2)
	print(result.stdout)


def scan_list_ports_nmap(ip, ports): 
	result = subprocess.run(['nmap', '-PN','-p', f'{ports}',   ip], stdout = subprocess.PIPE, encoding='utf-8')  
	write_file = 'static/py/python_nmap/result_scan/nmap_' + str(today.date()) + '.txt' 
	with open(write_file, 'x') as f2:
		print(result.stdout, file=f2)
	print(write_file)


def scan_list_nmap_write_csv(network_range, ports): 
	mas_result = {}  
	array_up_ip = fping_all(network_range) 
	if array_up_ip:
		str_ar_ip = ' '.join(array_up_ip)  
		nm = nmap.PortScanner()
		nm.scan(hosts=network_range, ports=ports, arguments='-sS --open')  # Scan ports 80 to 443,  -sU: UDP сканирование
		save_csv = nm.csv()   
		hosts = nm.all_hosts()     
		#save_file_from_csv = 'static/py/python_nmap/result_scan/csv_' + str(today.date()) + '.csv'
		#with open(save_file_from_csv, mode="a", newline="", encoding="utf-8") as file:
		#	file.write(save_csv[96::])
		for ip in hosts:
			array_up_ip.remove(ip)
			proto_ports = '' 
			for protocol in  nm[ip].all_protocols(): 
				list_ports = list(nm[ip][protocol].keys())  
				proto_ports = ', '.join(map(str, list_ports)) if len(list_ports) > 1 else str(list_ports[0])  
			
			text_other = create_visual_response_others(nm[ip]) 
			mas_result[ip] = {
				'ip': ip, 
				'port': proto_ports,
				'other': text_other, 
			} 
		if len(array_up_ip) > 0:
			for ip_not_port in array_up_ip:
				mas_result[ip_not_port] = {
					'ip': ip_not_port, 
					'port': '',
					'other': '', 
				}
		return mas_result
	else:
		return False


def create_visual_response_others(objects_ip):   
	try:
		text_rezult_ALL = f"IP Address: {objects_ip['addresses']['ipv4']}\n"
		text_rezult_ALL += f"MAC Address: {objects_ip['addresses']['mac']}\n"
		text_rezult_ALL += f"Vendor: {objects_ip['vendor'][objects_ip['addresses']['mac']]}\n"
		text_rezult_ALL += f"Host Status: {objects_ip['status']['state']}\n"
		text_rezult_ALL += f"Status Reason: {objects_ip['status']['reason']}\n" 
		if 'tcp' in objects_ip:
			text_rezult_ALL += "Open Ports TCP:\n"
			for port, info in objects_ip['tcp'].items():
				text_rezult_ALL += f"\tPort: {port}\n"
				text_rezult_ALL += f"\t  - State: {info['state']}\n"
				text_rezult_ALL += f"\t  - Service Name: {info['name']}\n"
				text_rezult_ALL += f"\t  - Product: {info['product']}\n"
				text_rezult_ALL += f"\t  - Version: {info['version']}\n"
				text_rezult_ALL += f"\t  - Extra Info: {info['extrainfo']}\n"
				text_rezult_ALL += f"\t  - Confidence: {info['conf']}\n"
				text_rezult_ALL += f"\t  - CPE: {info['cpe']}\n"  
		if 'udp' in objects_ip:
			text_rezult_ALL += "Open Ports UDP:\n"
			for port, info in objects_ip['udp'].items():
				text_rezult_ALL += f"\tPort: {port}\n"
				text_rezult_ALL += f"\t  - State: {info['state']}\n"
				text_rezult_ALL += f"\t  - Service Name: {info['name']}\n"
				text_rezult_ALL += f"\t  - Product: {info['product']}\n"
				text_rezult_ALL += f"\t  - Version: {info['version']}\n"
				text_rezult_ALL += f"\t  - Extra Info: {info['extrainfo']}\n"
				text_rezult_ALL += f"\t  - Confidence: {info['conf']}\n"
				text_rezult_ALL += f"\t  - CPE: {info['cpe']}\n"  
		return text_rezult_ALL
	except:
		return False

def create_obj_ip_to_bd_nmap(dict_ips): 
	result_obg_with_ips = {}  
	for ip in dict_ips:    
		result_obg_with_ips[ip] = {
		'ip'	   : ip,
		'update'   : today,
		'comments' : '',
		'checked'  : False,
		'id_svmap' : {
			'ports'	   : dict_ips[ip]['port'],
			'version'  : '',
			'dev_name' : '',
		},
		'id_nmap' : {
			'other'    : dict_ips[ip]['other'],
		}, 
		} 
	return result_obg_with_ips


def scan_list_nmap_and_result(ips, ports): 
	#виконуємо пошук та  записуємо  результат в тимчасовий обєкт
	obj_from_scan_nmap = scan_list_nmap_write_csv(ips, ports) 
	#створюємо словник який потім зможемо використовувати для запису в БД
	ips_to_bd = create_obj_ip_to_bd_nmap(obj_from_scan_nmap)
	return ips_to_bd



if __name__ == '__main__':
	network = '192.168.1.0/24'
	scan_network(network)
	
