from static.py.python_nmap.exam_fping import ping_all_ip_result_object
from static.py.python_nmap.scan_svmap import up_scan_svmap_and_result
from static.py.python_nmap.scan_nmap import scan_list_ports_nmap, scan_list_nmap_and_result



#Спочатку дізнаємось який саме пошук необхідно зробити
def chehekValueScan(valueObj):
	metodWork = valueObj.get('work')
	ip = valueObj.get('name') 
	match metodWork:
		case 'fping':
			try:
				res_scan_fping = ping_all_ip_result_object(ip)
				print('res_scan_fping')
				return res_scan_fping
			except:
				return False
		case 'svmap':
			try:
				print('svmap')
				obj_scan_ips = up_scan_svmap_and_result(ip) 
				return obj_scan_ips
			except:
				return False
		case 'listports': 
			try:
				print('listports') 
				port = valueObj.get('value')
				obj_scan_ips = scan_list_nmap_and_result(ip, port)  
				return obj_scan_ips
			except:
				return False
		case 'allports': 
			try:
				print('allports') 
				port = valueObj.get('value')
				obj_scan_ips = scan_list_nmap_and_result(ip, port)  
				return obj_scan_ips
			except:
				return False
		case _:
			return False
