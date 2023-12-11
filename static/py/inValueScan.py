from static.py.python_nmap.exam_fping import ping_all_ip_result_object
from static.py.python_nmap.scan_svmap import up_scan_svmap_and_result
from static.py.python_nmap.scan_nmap import scan_list_ports_nmap, scan_list_nmap_and_result, scan_nmap_all_ports_and_result, scan_masscan_port



# Спочатку дізнаємось який саме пошук необхідно зробити
# valueObj обеєкт { 'name' : '192..', 'work': 'listports', 'value': '80, 443'   }
def chehekValueScan(valueObj):
	metodWork = valueObj.get('work')					# розбираємо обеєкт
	ip = valueObj.get('name')
	match metodWork:
		case 'fping':												# виконується якщо дія fping
			try:
				res_scan_fping = ping_all_ip_result_object(ip) 		# визивається ф-я в якій всі скрипти пінгування
				print('res_scan_fping')
				return res_scan_fping								# повертає в на Бекенд обект
			except Exception as er:									# якщо помилка
				print('Відбулась помилка ;', er)
				return False
		case 'svmap':
			try:
				print('svmap')
				obj_scan_ips = up_scan_svmap_and_result(ip)
				if obj_scan_ips == False:							# якщо результатів немає то повертає пустий обєкт
					return {}
				return obj_scan_ips
			except Exception as er:
				print('Відбулась помилка ;', er)
				return False
		case 'listports':
			try:
				print('listports')
				port = valueObj.get('value')						# визначає які порти передали для сканування
				# obj_scan_ips = scan_list_nmap_and_result(ip, port)
				obj_scan_ips = scan_masscan_port(ip, port)
				return obj_scan_ips
			except Exception as er:
				print('Відбулась помилка ;', er)
				return False
		case 'allports':
			try:
				print('allports')
				port = valueObj.get('value')						# визначає які порти передали для сканування
				# obj_scan_ips = scan_list_nmap_and_result(ip, port)
				obj_scan_ips = scan_masscan_port(ip, port)
				return obj_scan_ips
			except Exception as er:
				print('Відбулась помилка ;', er)
				return False
		case 'pnports':
			try:
				print('pnports')
				obj_scan_ips = scan_nmap_all_ports_and_result(ip)
				return obj_scan_ips
			except Exception as er:
				print('Відбулась помилка ;', er)
				return False
		case _:
			return False
