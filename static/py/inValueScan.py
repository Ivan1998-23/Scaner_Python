from static.py.python_nmap.exam_fping import fping_all, fping_all_from_windows



#Спочатку дізнаємось який саме пошук необхідно зробити
def chehekValueScan(valueObj):
    metodWork = valueObj.get('work')
    match metodWork:
        case 'fping':
            ip = valueObj.get('name')
            print(ip)
            return fping_all(ip)
        case 'svmap':
            print('svmap')
            return True
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
