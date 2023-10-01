from ast import dump
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
# from static.py.bd import crStatusTF

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 's'
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbscan.db'
db = SQLAlchemy(app)

# Клас  ІР
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(25), nullable=False, unique=True)
    update = db.Column(db.DateTime, default=datetime.utcnow)               # остання дата перевірки
    created = db.Column(db.DateTime, nullable=True)                        # дата створення
    comments = db.Column(db.Text, nullable=True)                           # власні коменти
    checked = db.Column(db.Boolean, nullable=True)                         # подавали порушення
    id_svmap = db.relationship('Svmap', backref='address', uselist=False)  # Связь с профилем пользователя   1:1
    id_nmap = db.relationship('Nmap', backref='address', uselist=False)    # Связь с профилем пользователя   1:1
    id_status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)    # m:1
    def __repr__(self):
        return f'<Address {self.id}>'

# Клас описує які є порти та версію пристрою. відношення 1:1 до ІР
class Svmap(db.Model):
    __tablename__ = 'svmap'
    id = db.Column(db.Integer, primary_key=True)
    ports = db.Column(db.String(255), nullable=True)            # 80, 443, 21
    version = db.Column(db.String(50), nullable=True)           # Grandstream Dinstar Cisco
    dev_name = db.Column(db.String(50), nullable=True)          # ht818
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

# Клас який описує статус ІР включений чи ні. Відношення до ІР м:1
class Status(db.Model):      # 1:m
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Boolean, nullable=True)            # включен чи ні  up down
    id_address = db.relationship('Address', backref='status', lazy=True)  # Связь с постами пользователя

    def __repr__(self):
        return f'<Value {self.value}>'


# перевіряє чи створені два значення True False в таблиці Status




def crStatusTF():
    nstatus = Status.query.all()
    if len(nstatus) == 0:
        status_tr = Status(value=True)
        status_fl = Status(value=False)
        db.session.add(status_tr)
        db.session.add(status_fl)
        db.session.commit()


with app.app_context():
    crStatusTF()         # створюємо в БД дві змінні ТРУ та Фолс
    db.create_all()

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
        address_from_com = Address.query.get(id_com)
        comments = data.get('comments')
        if comments is not None:
            address_from_com.comments = comments
        else:
            value = data.get('value')
            address_from_com.checked = value
        db.session.add(address_from_com)
        db.session.commit()
    return render_template("index.html", address=address)


@app.route("/addIP", methods=['POST', 'GET'])
def addIP():
    if request.method == "POST":
        # варіант коли запити йдуть від JS
        checked = False
        data = request.get_json()
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
                new_ip = Address(ip=ip, comments=comment, checked=checked, status=Status.query.get(1))
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

        # # ввариант когда бекенд сразу загружает все с сайта
        # checked = False
        # violations = request.form['violations']
        # ip = request.form['ip']
        # port = request.form['port']
        # comment = request.form['comment']
        # if violations == 'Yes':
        #     checked = True
        # try:
        #     if len(Address.query.filter_by(ip=ip).all()) == 0:
        #         new_ip = Address(ip=ip, comments=comment, checked=checked, status=Status.query.get(1))
        #         new_svmap = Svmap(ports=port, address=new_ip)
        #         new_nmap = Nmap(other='', address=new_ip)
        #         db.session.add_all([new_svmap, new_nmap, new_ip])
        #         db.session.commit()
        #         return render_template("addIP.html")
        #     else:
        #         return render_template("errorAddIP.html", massedg='Tакий ІР вже є')
        # except:
        #     return render_template("errorAddIP.html", massedg='Щось ввели не те')
    else:
        return render_template("addIP.html")


@app.route("/findIP", methods=['POST', 'GET'])
def findIP():
    # if request.method == "POST":
    #     title = request.form['ipadress']
    #     print(title)
    # else:
    return render_template("findIP.html")

@app.route('/statistics')
def statistics():
    return '<h1>Hello World!</h1>'



if __name__ == '__main__':
    app.run(debug=True)
