import sys
import subprocess
import csv 
from datetime import datetime
today = datetime.now()

# функція пінгує хости і дописує активні хости в файл output_scv.csv
# обов'язково вписувати адресу з маскою через /
# Приклад виклику ф-і :   python exam_fping.py 192.168.100.1/28
def fping_all(address): 
	'''
	today = date.today()
	write_file = 'static/py/python_nmap/result_scan/' + str(today) + '.txt' 
	''' 
	# якщо передається з маскою  ('/')   то ставимо арнумент -g
	if '/' in address:
		result = subprocess.run(['fping', '-r', '2', '-a', '-g',  address], stdout = subprocess.PIPE)
	else:
		result = subprocess.run(['fping', '-r', '2', '-a', address], stdout = subprocess.PIPE)
	mas_alive = result.stdout.decode('utf-8').split('\n')
	mas_alive.remove('')
	if len(mas_alive) == 0:
		return False
	else:
		'''
		with open(write_file, 'a') as f2:
			for row in mas_alive:
				print(row, file=f2)
			print('', file=f2)
		'''  
		return mas_alive

# пінгує з ОС windows
def fping_all_from_windows (address):
	result = subprocess.run(["ping", address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	# Отримати висновок ping
	ping_output = result.stdout
	print(ping_output)


# створюємо словник який потім зможемо використовувати для запису в БД
def create_obj_fping_ip_to_bd(array_ips):
	result_obg_with_ips = {} 
	for ip in array_ips:   
		result_obg_with_ips[ip] = {
		'ip'	   : ip,
		'update'   : today,
		'comments' : '',
		'checked'  : '',
		'id_svmap' : {
			'ports'	   : '',
			'version'  : '',
			'dev_name' : ''
		},
		'id_nmap' : {
			'other'    : ''
		}, 
		} 
	return result_obg_with_ips


def ping_all_ip_result_object(ip):
	ob_ip = fping_all(ip)
	if ob_ip:
		return create_obj_fping_ip_to_bd(ob_ip)
	else:
		return False


if __name__ == '__main__':
	address = sys.argv[1]
	fping_all(address)

'''
'id_nmap' : {
			'other'    : '
		Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-30 12:12 EDT
		Nmap scan report for 192.168.1.1
		Host is up (0.0052s latency).

		PORT     STATE    SERVICE
		22/tcp   open     ssh
		80/tcp   open     http
		443/tcp  filtered https
		5060/tcp filtered sip
		5062/tcp filtered na-localise
		8080/tcp filtered http-proxy'
		}, 
'''
