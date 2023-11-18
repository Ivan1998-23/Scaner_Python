import sys
import subprocess
import csv
from datetime import datetime
import re


today = datetime.now()

result_svmap = '''+--------------------+-------------------------------------+
| SIP Device         | User Agent                          |
+====================+=====================================+
| 10.180.25.23:5060  | Grandstream GXP1620 1.0.7.50        |
+--------------------+-------------------------------------+
| 10.180.25.23:5062  | Grandstream GXP1620 1.0.7.50        |
+--------------------+-------------------------------------+
| 10.184.82.28:5060  | Grandstream GXW4216  V2.3B 1.0.23.5 |
+--------------------+-------------------------------------+
| 10.184.82.28:5062  | Grandstream GXW4216  V2.3B 1.0.23.5 |
+--------------------+-------------------------------------+
| 10.189.82.101:5060 | Grandstream GXP1625 1.0.7.49        |
+--------------------+-------------------------------------+
| 10.189.82.101:5062 | Grandstream GXP1625 1.0.7.49        |
+--------------------+-------------------------------------+'''


#виконуємо пошук та зберігаємо весь текст результату
def svmap_SIP(address):  
    name_file = 'svmap_'+ str(today) 
    write_file = 'result_scan/' + name_file + '.txt' 
    
    result = subprocess.run(['svmap', '-p5060-5062',  address], stdout = subprocess.PIPE)
    all_text = result.stdout.decode('utf-8') 
    '''
    with open(write_file, 'a') as f2:
        print(all_text, file=f2)
        print('', file=f2) 
    '''
    return all_text

#регулярні вирази дозволяють вибрати необхідне з великого тексту
def search_regular_expression(in_str): 
	#використовуємо регулярний вираз щоб вибрати те що нам треба
	regex= r' +(?P<ip>\d+\.\d+\.\d+\.\d+):(?P<port>\d+) +\| +(?P<name>\S+) (?P<name_v>\S+) (?P<version>.*) \|'
	#result = [match.groups() for match in re.finditer(regex, in_str)]
	 
	#створюємо новий обєкт в якому ІР буде ключом  
	mas_result = {}
	#перебираємо текст построчно
	for line in in_str.split('\n'): 
		match = re.search(regex, line)
		#якщо спрацьовує регулярний вираз 
		if match: 
			inf_ip = match.groupdict()
			inf_ip['other'] = line.strip()
			# Видаляємо зайві пробіли в кінці та на початку
			inf_ip['version'] = inf_ip.get('version').strip() 
			#додаємо інфу або змінюємо  таку ж інфу
			find_ip_in_dict = mas_result.get(inf_ip['ip']) 
			if find_ip_in_dict: 
				if inf_ip['port'] == '':
					inf_ip['port'] = find_ip_in_dict.get('port')
				else:
					inf_ip['port'] += ', ' +find_ip_in_dict.get('port')
				lin_tab = '-' * len(line)
				inf_ip['other'] += '\n' + find_ip_in_dict.get('other')+ '\n' + lin_tab  
				#inf_ip['other'] += '\n' + find_ip_in_dict.get('other')
			mas_result[inf_ip['ip']] = inf_ip  
	return mas_result 
	'''
	 mas_result = 
	{'10.180.25.23': {
	'ip': '10.180.25.23', 
		'port': '5062', 
		'name': 'Grandstream',
		'name_v': 'GXP1620', 
		'version': '1.0.7.50'
	},
	'10.184.82.28': {
		'ip': '10.184.82.28', 
		'port': '5062', 
		'name': 'Grandstream', 
		'name_v': 'GXW4216', 
		'version': 'V2.3B 1.0.23.5'
	}
	'''									
	
#створюємо словник який потім зможемо використовувати для запису в БД    
def create_obj_ip_to_bd(dict_ips):
	result_obg_with_ips = {}  
	for ip in dict_ips:   
		ports_coma = dict_ips[ip]['port'] 
		print('ports_coma', ports_coma)
		result_obg_with_ips[ip] = {
		'ip'	   : ip,
		'update'   : today ,
		'comments' : '',
		'checked'  : False,
		'id_svmap' : {
			'ports'	   : ports_coma,
			'version'  : dict_ips[ip]['version'],
			'dev_name' : dict_ips[ip]['name']+ ' '  + dict_ips[ip]['name_v']
		},
		'id_nmap' : {
			'other'    : dict_ips[ip]['other'],
		}, 
		} 
	return result_obg_with_ips
		
def up_scan_svmap_and_result(ips):
	#виконуємо пошук та зберігаємо весь текст результату
	text = svmap_SIP(ips)
	print(text)
	#вибираємо необхідне  
	dict_with_ips = search_regular_expression(text)
	#створюємо словник який потім зможемо використовувати для запису в БД
	ips_from_bd = create_obj_ip_to_bd(dict_with_ips) 
	print(ips_from_bd)
	return  ips_from_bd if ips_from_bd != {} else False


if __name__ == '__main__':
	address = sys.argv[1]
	#svmap_SIP(address)
	ips_from_bd = create_obj_ip_to_bd(search_regular_expression(result_svmap))
	print(ips_from_bd)
