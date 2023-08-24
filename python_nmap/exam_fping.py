import sys
import subprocess
import csv

address = sys.argv[1]

#функция пингует хосты и дописывает активные хосты в файл output_scv.csv
#обязательно вписывать адрес с маской через /
# Пример вызова ф-и :   python exam_fping.py 192.168.100.1/28
def fping_all(address):
    '''
    command = 'fping' 
   # result = subprocess.run([command, '-g', '-c', '4',  address], stdout = subprocess.DEVNULL, encoding = 'utf-8')
    result = subprocess.run([command, '-c', '4', address])
    print([command,address])
    print(result.stdout)
    with open('output.txt', 'a') as f:
        print(result.stdout, file=f)
    '''
    
    result = subprocess.run(['fping', '-g',  address], stdout = subprocess.PIPE)
    
    mas = result.stdout.decode('utf-8').split('\n')
    mas_alive = []
    for element in mas:
        if 'alive' in element:
            mas_alive.append(element.split()[0])
    
    with open('output_in_txt.txt', 'a') as f2:
        for row in mas_alive:
            print(row, file=f2)
     
          
if __name__ == '__main__':
    fping_all(address)
