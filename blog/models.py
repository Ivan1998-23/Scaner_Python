from blog import db
from datetime import datetime



# Клас  ІР
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(25), nullable=False, unique=True)
    update = db.Column(db.DateTime, default=datetime.now)               # остання дата перевірки
    created = db.Column(db.DateTime, default=datetime.now)              # дата створення
    violation = db.Column(db.Text, default='', nullable=True)           # порушення які виявили
    comments = db.Column(db.Text, default='', nullable=True)               # Примітки
    password = db.Column(db.Text, default='', nullable=True)            # password
    checked = db.Column(db.Boolean, nullable=True)                         # подавали порушення
    looked = db.Column(db.Boolean, default=False, nullable=True)           # чи взагалі перевіряли його 
    id_svmap  = db.relationship('Svmap', backref='address', uselist=False)  # Связь с профилем пользователя   1:1
    id_nmap = db.relationship('Nmap', backref='address', uselist=False)    # Связь с профилем пользователя   1:1 
    status = db.Column(db.Boolean, default=True, nullable=False)            # включен чи ні  up down
    def __repr__(self):
        return f'<Address {self.id}>'



# Клас описує які є порти та версію пристрою. відношення 1:1 до ІР
class Svmap(db.Model):
    __tablename__ = 'svmap'
    id = db.Column(db.Integer, primary_key=True)
    ports = db.Column(db.String(255), nullable=True)            # 80, 443, 21
    version = db.Column(db.String(50), nullable=True)           # 1.0.7.13
    dev_name = db.Column(db.String(50), nullable=True)          # Grandstreamht818 Dinstar Cisco
    id_address = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True, nullable=False)

    def __repr__(self):
        return f'<Ports {self.id}>'



# Клас який описує все що сканував nmap
class Nmap(db.Model):
    __tablename__ = 'nmap'
    id = db.Column(db.Integer, primary_key=True)
    other = db.Column(db.Text, nullable=True)            # nmap result scan......
    id_address = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True, nullable=False)

    def __repr__(self):
        return f'<Other {self.id}>'



class LogScan(db.Model):
    __tablename__ = 'logscan'
    id = db.Column(db.Integer, primary_key=True) 
    start_time = db.Column(db.DateTime, default=datetime.now)           # дата створення
    ips = db.Column(db.String(25), nullable=False)
    result = db.Column(db.Boolean, nullable=True)           	 		#  True  or False
    command = db.Column(db.String(20), nullable=True)            		# fping nmam svmap
    other = db.Column(db.String(255), nullable=True)            		# nmap result scan......

    def __repr__(self):
        return f'<LogScan {self.id}>'



#перзаписуємо значення ІР
def update_address_from_data(id_ones_ip, data): 
    # Визначте, які поля в класах потрібно оновити
    address_fields = ['ip', 'update',    'checked']
    svmap_fields = ['ports', 'version', 'dev_name']
    nmap_fields = ['other']
    try: 
        #Оновіть поля класу Address на основі даних
        for field in address_fields: 
            if field in data and data[field] != '':   
                setattr(id_ones_ip, field, data[field])
		# Оновіть поля класу Svmap на основі даних з id_svmap
        svmap = id_ones_ip.id_svmap 	        
        for field in svmap_fields: 
            if field in data['id_svmap'] and data['id_svmap'][field] != '': 
                filtr_ports = data['id_svmap'][field]  
                if field == 'ports': 
                    ar1 = svmap.ports
                    ar2 = data['id_svmap'][field]         
                    filtr_ports = remove_repits_port(ar1, ar2)             
                setattr(svmap, field, filtr_ports) 
		
		# Оновіть поля класу Nmap на основі даних з  id_nmap
        nmap = id_ones_ip.id_nmap    
        #for field in nmap_fields: 
        #    if field in data['id_nmap'] and data['id_nmap'][field] != '' : 
        #        if field == 'other':
        #            current_text = f'\n------{datetime.now().strftime("%Y.%m.%d %H:%M")}----------\n'
        #            current_text += data['id_nmap'][field]  +'\n'
        #            current_text += nmap.other 
        #        setattr(nmap, field, current_text)    

        if data['id_nmap']['other'] != '' :  
            current_text = f'\n------{datetime.now().strftime("%Y.%m.%d %H:%M")}----------\n'
            current_text += data['id_nmap']['other']  +'\n'
            current_text += nmap.other 
            #перевіряє якщо стало більше 3000 символів то обрізати все що більше 3000
            if len(current_text) > 3000:
                current_text = current_text[0:3000]
            setattr(nmap, 'other', current_text)  
        db.session.add(id_ones_ip)
    except Exception as er:
        print('помилка в перезаписі значень')
        print(er)


# вирізаємо з двох масивів однакові порти та записуємо в один масив
def remove_repits_port(ar1, ar2):
	try:  
		if ar1 == '':
			result = ar2
		else:
			list_ar1 = ar1.split(', ')
			list_ar2 = ar2.split(', ') 
			all_array = list_ar1 + list_ar2   
			result_set = set(all_array)   
			result_ar = list(result_set)  
			result = ', '.join(result_ar) 
		
		return result
	except Exception as er:
		print('помилка в обєднанні списку портів')
		print(er)



# Записуємо  новий ІР
def create_address_from_data(ip, data):  
    new_ip = Address(ip=ip, comments=data['comments']) 
    new_svmap = Svmap(
				ports=data['id_svmap']['ports'],
				version=data['id_svmap']['version'],
				dev_name=data['id_svmap']['dev_name'] ,
				address=new_ip)  
    if  len(data['id_nmap']['other']) > 1:
        other_add_time = f'\n------{datetime.now().strftime("%Y.%m.%d %H:%M")}----------\n'
        other_add_time += data['id_nmap']['other']
    else:
        other_add_time = data['id_nmap']['other']
    new_nmap = Nmap(other=other_add_time, address=new_ip)
    db.session.add_all([new_svmap, new_nmap, new_ip])
	

# Записуємо логи сканування 
def create_log_scan_ips(valueObj, resul_b):  
    metodWork = valueObj.get('work')
    ips = valueObj.get('name')
    match metodWork:
        case 'fping':
            other = 'ping'
        case 'svmap':
            other = '5060-5062'
        case 'listports':
            other = valueObj.get('value')
        case 'allports':
            other = valueObj.get('value')  
        case 'pnports':
            other = '0-1000'  
	
    #other = valueObj.get('value') if valueObj.get('value')  else ''
     
    new_log = LogScan(ips = ips, result = resul_b, command = metodWork, other = other) 
    
    db.session.add(new_log) 
    db.session.commit() 
