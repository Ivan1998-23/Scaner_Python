from ast import dump
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import StringField, SubmitField
from static.py.inValueScan import chehekValueScan
import json
import urllib.parse

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 's'
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbscan.db'
db = SQLAlchemy(app)


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
    id_svmap = db.relationship('Svmap', backref='address', uselist=False)  # Связь с профилем пользователя   1:1
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


with app.app_context():
    #crStatusTF()         # створюємо в БД дві змінні ТРУ та Фолс
    db.create_all()


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
	




@app.route('/errorAddIP', methods=['POST', 'GET'])
def errorAddIP():
    return render_template('errorAddIP.html')

@app.route("/home", methods=['POST', 'GET'])
@app.route("/", methods=['POST', 'GET'])
def index():
    address = Address.query.all()
    # коли робимо якісь зміни в comments та зміні флажка то вони автоматично зберігаються
    if request.method == "POST":
        data = request.get_json()
        id_com = data.get('id')
        work = data.get('work')
        response_data = {}
        try:
            address_from_com = Address.query.get(id_com)  
            match work:
                case 'com':   #дадаємо коменти
                    comments = data.get('comments')
                    address_from_com.comments = comments
                    db.session.add(address_from_com)
                case 'vio':   #дадаємо коменти
                    comments = data.get('comments')
                    address_from_com.violation = comments
                    db.session.add(address_from_com)
                case 'chek': # змінюємо значення чи подавали порушення
                    value = data.get('value') 
                    address_from_com.checked = value
                    db.session.add(address_from_com)
                case 'look': # змінюємо значення чи подавали порушення
                    value = data.get('value') 
                    address_from_com.looked = value
                    db.session.add(address_from_com)
                case 'del':  # видаляємо спочатку значення з таблиць nmap, svmap а потім вже ІР
                    if address_from_com:
                        delet_list_ip_svmap_ = address_from_com.id_svmap
                        if delet_list_ip_svmap_:
                            db.session.delete(delet_list_ip_svmap_)
                            print('delete',  delet_list_ip_svmap_)

                        delet_list_ip_nmap = address_from_com.id_nmap
                        if delet_list_ip_nmap:
                            db.session.delete(delet_list_ip_nmap)
                            print('delete', delet_list_ip_nmap)
                        db.session.delete(address_from_com)
                        print('delete', address_from_com)
                        response_data = {"result": True}
                    else:
                        print('delete', address_from_com)
                        response_data = {"result": False}

                # case _:
                #     pass

            db.session.commit()
            return jsonify(response_data)
        except:
            return 'Відбулись якісь проблеми'
    return render_template("index.html", address=address)


@app.route("/addIP", methods=['POST', 'GET'])
def addIP():
    if request.method == "POST": 
        # варіант коли запити йдуть від JS
        checked = False
        data = request.get_json()
        print('OK')
        ip = data.get('ip')
        port = data.get('port')
        comment = data.get('comment')
        violations = data.get('violations')
        
        if violations == 'Yes':
            checked = True
        try:
            # Робимо пошук в БД всі тікі ІР  та записуємо в масив
            findListIPFromBD = len(Address.query.filter_by(ip=ip).all())
            # якщо в масиві 0 елементів значить нічого не знайшли і такий ІР унікальний
            if findListIPFromBD == 0:
                # Записуємо ІР в  БД
                new_ip = Address(ip=ip, comments=comment, checked=checked)
                new_svmap = Svmap(ports=port, address=new_ip)
                new_nmap = Nmap(other='', address=new_ip)
                db.session.add_all([new_svmap, new_nmap, new_ip])
                db.session.commit() 
                # Повертаємо на фронт True, для підтвердження запису в БД
                response_data = {"result": True}
            else:
                # Якщо Ір не унікальний то повідомляємо про не унікальність ІР
                response_data = {"result": False}
            return jsonify(response_data)
        except:
            return 'Відбулись якісь проблеми'
    else:
        return render_template("addIP.html")


@app.route("/findIP", methods=['POST', 'GET'])
def findIP():
    if request.method == "POST":
        data = request.get_json() 
        return_data = chehekValueScan(data)  
        #Перевіряємо що повернула ф-я виконання сканування 
        if  return_data == False :
            response_data = {"result": False}
            return jsonify( response_data)
        #print('return_data: ',return_data)
        try:
			# Беребираємо список ІР
            for key_ip, val_ip in return_data.items():	 
			    # шукаємо чи є тіки ІР в БД та показуємо кількість співпадінь
                findListIPFromBD = len(Address.query.filter_by(ip=key_ip).all())
                # якщо в масиві 0 елементів, значить ІР унікальний 
                if findListIPFromBD == 0:
                    # Записуємо  новий ІР   
                    create_address_from_data(key_ip, val_ip)  
                else: 
					#перезаписуємо значення в ІР
                    id_ones_ip = Address.query.filter_by(ip=key_ip).first() 
                    update_address_from_data(id_ones_ip, val_ip)  
                db.session.commit()  
                
            response_data = {"result": return_data}
            print('return result from findIP')
            print(return_data)
            return jsonify( response_data)
        except:
             return 'Відбулись якісь проблеми' 
        
        response_data = {"result": return_data}
        return jsonify(response_data)
        # return render_template("findIP.html")
    else:
        return render_template("findIP.html")

@app.route('/statistics')
def statistics():
    return '<h1>Hello World!</h1>'

@app.route("/resultFindIPs", methods=['GET'])
def resultFindIPs():
    data_param = request.args.get('data')  
    if data_param:
        # Перетворіть дані назад із рядка JSON
        response_data = json.loads(urllib.parse.unquote(data_param))
        # Kод для відображення даних на новій сторінці
        #print('result', response_data)
        return render_template('resultFindIPs.html', data=response_data.get('result'))
    else:
        return "Дані не знайдено" 

if __name__ == '__main__':
    app.run(debug=True)
