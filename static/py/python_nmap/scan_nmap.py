import nmap
import csv
from datetime import datetime
import subprocess
from static.py.python_nmap.exam_fping import fping_all 
import re

today = datetime.now()
ports_from_server = ["22","80", "443", "5060", "5062", "8080"]
ports_from_windows = ["3389", "25", "445", "1433", "53", "67", "68", "161", "162", "139", "135"]

# скануємо та записуємо до файлу 'result_scan/csv_' + str(today) + '.csv'
def scan_nmap_write_csv(network_range):
	today = datetime.today()
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


# скануємо на готовий список портів
def scan_network(network_range):
	port = ', '.join(ports_from_windows)
	port2 = ', '.join(ports_from_server)
	write_file = 'result_scan/nmap_' + str(today) + '.txt'
	result = subprocess.run(['nmap', '-p', f'{port2}',   network_range], stdout=subprocess.PIPE, encoding='utf-8')
	with open(write_file, 'w') as f2:
		print(result.stdout, file=f2) 

# скануємо на  список портів які передали до ф-ї
def scan_list_ports_nmap(ip, ports):
	result = subprocess.run(['nmap', '-PN', '-p', f'{ports}',   ip], stdout=subprocess.PIPE, encoding='utf-8')
	write_file = 'static/py/python_nmap/result_scan/nmap_' + str(today.date()) + '.txt'
	with open(write_file, 'x') as f2:
		print(result.stdout, file=f2) 


#скануємо всі порти за допомогою nmap
def scan_nmap(ip): 
	try: 
		result = subprocess.run(['nmap', ip], stdout = subprocess.PIPE, encoding='utf-8')   
		text = result.stdout 
		pars_obg = find_regular_in_scan_nmap(text)
		return pars_obg
	except Exception as er:
		print('помилка в скануванні на всі порти')
		print(er)


#регулярний вираз який буде шукати ІР та порти в повному тексті
def find_regular_in_scan_nmap(all_text): 
	regex_ip= r'Nmap scan report for (?P<ip>\d+\.\d+\.\d+\.\d+)' 
	regex_port= r'(?P<ports>\d+)\/(?P<type>\S+) +(?P<status>\S+)' 
	#result = [match.groups() for match in re.finditer(regex, in_str)]
	#створюємо новий обєкт в якому ІР буде ключом  
	mas_result = {}
	ob_ip = {
		'ip': '',
		'ports': '',
		'other': ''
	} 
	#перебираємо текст построчно
	for line in all_text.split('\n'): 
		match = re.search(regex_ip, line) 
		if match:
			inf_ip = match.groupdict()
			ip = inf_ip['ip']
			ob_ip['ip'] = ip
			ob_ip['ports'] = ''
			ob_ip['other'] = line +'\n'
			mas_result[ip] = ob_ip
		else:
			match_port = re.search(regex_port, line) 
			if match_port:  
				inf_port = match_port.groupdict()  
				ports = inf_port['ports']
				if len(ob_ip['ports']) > 0:
					ob_ip['ports'] = ob_ip['ports'] + ', ' + inf_port['ports']
				else:
					ob_ip['ports'] = inf_port['ports'] 
			if len(mas_result) !=0:
				mas_result[ob_ip['ip']]['other'] += line +'\n'  
	return mas_result   


# скануємо на  список портів які передали та записуєио результат в файл
# повертає обєкт в якому зберігається вся інформація про ІР
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
			for protocol in nm[ip].all_protocols():
				list_ports = list(nm[ip][protocol].keys())
				proto_ports = ', '.join(map(str, list_ports)) if len(list_ports) > 1 else str(list_ports[0])

			text_other = create_visual_response_others(nm[ip]) 
			mas_result[ip] = {
				'ip': ip,
				'ports': proto_ports,
				'other': text_other,
			}
		if len(array_up_ip) > 0:
			for ip_not_port in array_up_ip:
				mas_result[ip_not_port] = {
					'ip': ip_not_port,
					'ports': '',
					'other': '',
				}
		return mas_result
	else:
		return False


def masscan_scan(ips, ports='0-65535'): 
	result = subprocess.run(['masscan', '-p', f'{ports}',   ips], stdout = subprocess.PIPE, encoding='utf-8')  
	all_text = result.stdout  
	# використовуємо регулярний вираз щоб вибрати те що нам треба
	regex= r'\S+ +(?P<status>\S+) +\S+ +(?P<ports>\d+)\/(?P<type>\S+) +\S+ +(?P<ip>\d+\.\d+.\d+.\d+)' 
	# result = [match.groups() for match in re.finditer(regex, in_str)]
	 
	# створюємо новий обєкт в якому ІР буде ключом
	mas_result = {}
	# перебираємо текст построчно
	for line in all_text.split('\n'):  
		match = re.search(regex, line) 
		# якщо спрацьовує регулярний вираз
		if match: 
			inf_ip = match.groupdict() 
			inf_ip['other'] = line.strip() 
			# додаємо  інфу PORT або змінюємо  таку ж інфу
			find_ip_in_dict = mas_result.get(inf_ip['ip'])   
			if find_ip_in_dict:  
				if inf_ip['ports'] == '': 
					inf_ip['ports'] = find_ip_in_dict.get('ports')
				else: 
					inf_ip['ports'] += ', ' + find_ip_in_dict.get('ports')  
				inf_ip['other'] += '\n' + find_ip_in_dict.get('other')   
			mas_result[inf_ip['ip']] = inf_ip   
	return mas_result 
'''
 mas_result = 
{'10.180.25.23': {
	'ip': '10.180.25.23', 
	'port': '5062', 
	'status': 'open',
	'type': 'tcp', 
	'other': 'Discovered open port 80/tcp on 10.187.95.69'
}}
'''

# Створюється візуальний варіант який записується в ОЗЕР
def create_visual_response_others(objects_ip):
	try: 
		text_rezult_ALL = f"IP Address: {objects_ip['addresses']['ipv4']}\n"
		# text_rezult_ALL += f"MAC Address: {objects_ip['addresses']['mac']}\n"
		text_rezult_ALL += f"Vendor: {objects_ip['vendor']}\n"
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

# Створюємо обєкт який буде записуватись в БД
def create_obj_ip_to_bd_nmap(dict_ips):
	try: 
		result_obg_with_ips = {}
		for ip in dict_ips:
			result_obg_with_ips[ip] = {
			'ip'	   : ip,
			'update'   : today,
			'comments' : '',
			'checked'  : False,
			'id_svmap' : {
				'ports'	   : dict_ips[ip]['ports'],
				'version'  : '',
				'dev_name' : '',
			},
			'id_nmap' : {
				'other'    : dict_ips[ip]['other'],
			},
			}
		return result_obg_with_ips
	except Exception as er:
		print('Помилка При створенні основного обекту для запису в БД')
		print(er)


def scan_list_nmap_and_result(ips, ports):
	# виконуємо пошук та  записуємо  результат в тимчасовий обєкт
	obj_from_scan_nmap = scan_list_nmap_write_csv(ips, ports)
	# створюємо словник який потім зможемо використовувати для запису в БД
	ips_to_bd = create_obj_ip_to_bd_nmap(obj_from_scan_nmap) 
	return ips_to_bd


def scan_masscan_port(ips, ports):
	#виконуємо пошук та  записуємо  результат в тимчасовий обєкт
	obj_from_scan_nmap = masscan_scan(ips, ports)  
	ips_to_bd = create_obj_ip_to_bd_nmap(obj_from_scan_nmap) 
	return ips_to_bd


def scan_nmap_all_ports_and_result(ips):
	#виконуємо пошук та  записуємо  результат в тимчасовий обєкт
	obj_from_scan_nmap = scan_nmap(ips)  
	#створюємо словник який потім зможемо використовувати для запису в БД
	ips_to_bd = create_obj_ip_to_bd_nmap(obj_from_scan_nmap) 
	return ips_to_bd


if __name__ == '__main__':
	network = '192.168.85.147'
	argument = '-A -Pn '
	print(scan_list_nmap_write_csv(network))

