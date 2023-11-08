import sys
import subprocess
import csv
from datetime import date

#функция пингует хосты и дописывает активные хосты в файл output_scv.csv
#обязательно вписывать адрес с маской через /
# Пример вызова ф-и :   python exam_fping.py 192.168.100.1/28
def fping_all(address): 
    today = date.today()
    write_file = 'result_scan/' + str(today) + '.txt' 
    result = subprocess.run(['fping', '-a', '-g',  address], stdout = subprocess.PIPE)
    
    mas_alive = result.stdout.decode('utf-8').split('\n') 
  
    with open(write_file, 'a') as f2:
        for row in mas_alive:
            print(row, file=f2)
        print('', file=f2)
          
if __name__ == '__main__':
	address = sys.argv[1] 
	fping_all(address)