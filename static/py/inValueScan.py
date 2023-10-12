from static.py.python_nmap.exam_fping import fping_all, fping_all_from_windows
from static.py.python_nmap.scan_svmap import up_scan_svmap_and_result



#Спочатку дізнаємось який саме пошук необхідно зробити
def chehekValueScan(valueObj):
	metodWork = valueObj.get('work')
	ip = valueObj.get('name') 
	match metodWork:
		case 'fping':
			try:
				res_scan_fping = fping_all(ip)
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
			print('listports')
			print(valueObj.get('value'))
			return True
		case 'allports':
			print('allports')
			print(valueObj.get('value'))
			return True
		case _:
			return False
