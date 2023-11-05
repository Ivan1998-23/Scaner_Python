from __init__ import db
from datetime import datetime
# Клас  ІР
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(25), nullable=False, unique=True)
    update = db.Column(db.DateTime, default=datetime.now)               # остання дата перевірки
    created = db.Column(db.DateTime, default=datetime.now)              # дата створення
    violation = db.Column(db.Text, default='', nullable=True)           # порушення які виявили
    comments = db.Column(db.Text, default='', nullable=True)               # Примітки
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
    other = db.Column(db.String(255), nullable=True)            # nmap result scan......
    id_address = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True, nullable=False)

    def __repr__(self):
        return f'<Other {self.id}>'

#перзаписуємо значення ІР
def update_address_from_data(id_ones_ip, data): 
    # Визначте, які поля в класах потрібно оновити
    address_fields = ['ip', 'update',    'checked']
    svmap_fields = ['ports', 'version', 'dev_name']
    nmap_fields = ['other']
    # Оновіть поля класу Address на основі даних
    for field in address_fields:
        if field in data and data[field] != '':  
            setattr(id_ones_ip, field, data[field])
    # Оновіть поля класу Svmap на основі даних з id_svmap
    svmap = id_ones_ip.id_svmap
    for field in svmap_fields:
        if field in data['id_svmap'] and data['id_svmap'][field] != '': 
            setattr(svmap, field, data['id_svmap'][field])
    # Оновіть поля класу Nmap на основі даних з  id_nmap
    nmap = id_ones_ip.id_nmap
    for field in nmap_fields: 
        if field in data['id_nmap'] and data['id_nmap'][field] != '' : 
            setattr(nmap, field, data['id_nmap'][field])
    db.session.add(id_ones_ip)


# Записуємо  новий ІР
def create_address_from_data(ip, data):  
	new_ip = Address(ip=ip, comments=data['comments'])   
	new_svmap = Svmap(
				ports=data['id_svmap']['ports'], 
				version=data['id_svmap']['version'],
				dev_name=data['id_svmap']['dev_name'] ,
				address=new_ip)   
	new_nmap = Nmap(other=data['id_nmap']['other'], address=new_ip) 
	db.session.add_all([new_svmap, new_nmap, new_ip]) 
	
