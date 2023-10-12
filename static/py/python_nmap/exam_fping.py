import sys
import subprocess
import csv
from datetime import date

today = date.today()

#функция пингует хосты и дописывает активные хосты в файл output_scv.csv
#обязательно вписывать адрес с маской через /
# Пример вызова ф-и :   python exam_fping.py 192.168.100.1/28
def fping_all(address): 
	'''
	today = date.today()
	write_file = 'static/py/python_nmap/result_scan/' + str(today) + '.txt' 
	'''
	result = subprocess.run(['fping', '-a', '-g',  address], stdout = subprocess.PIPE)
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
		#переводимо в зручний словник
		return create_obj_fping_ip_to_bd(mas_alive)
	
def fping_all_from_windows (address):
    result = subprocess.run(["ping", address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Получить вывод ping
    ping_output = result.stdout
    print(ping_output)


#створюємо словник який потім зможемо використовувати для запису в БД    
def create_obj_fping_ip_to_bd(array_ips):
	result_obg_with_ips = {} 
	for ip in array_ips: 
		result_obg_with_ips[ip] = {
		'ip'	   : ip,
		'update'   : today,
		'comments' : '',
		'ports'	   : '',
		'version'  : '',
		'dev_name' : '',
		'other'    : '' 
		} 
	return result_obg_with_ips

if __name__ == '__main__':
	address = sys.argv[1]
	fping_all(address)
