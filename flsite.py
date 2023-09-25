from ast import dump
from datetime import datetime
from tkinter.tix import Form
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 's'
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbscan.db'
db = SQLAlchemy(app)

# 1
class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(25), nullable=False, unique=True)
    # id_status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)                     # :m
    update = db.Column(db.DateTime, default=datetime.utcnow)
    created = db.Column(db.DateTime)
    # svmap = db.relationship('Device', backref='article', uselist=False)
    # nmap =
    comments = db.Column(db.Text, nullable=True)
    checked = db.Column(db.Boolean, nullable=True)
              # divice = db.relationship('Device', backref='article', uselist=False)

    def __repr__(self):
        return '<Address %r>' % self.id

# svmap
class Svmap(db.Model):
    __tablename__ = 'Svmap'
    id = db.Column(db.Integer, primary_key=True)
    ports = db.Column(db.String(255), nullable=True)
    version = db.Column(db.String(50), nullable=True)
    dev_name = db.Column(db.String(50), nullable=True)
    # article = db.relationship('Article', backref='device', uselist=False)

# fping scan        1:
# class Status(db.Model):
#     __tablename__ = 'status'
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Boolean, nullable=False, unique=True)
#     address = db.relationship('Address', backref='status', lazy=True)




@app.route("/home")
@app.route("/")
def index():
    address = Address.query.all()
    return render_template("index.html", address=address)


@app.route("/addIP", methods=['POST', 'GET'])
def addIP():
    if request.method == "POST":
        b = False
        violations = request.form['violations']
        ip = request.form['ip']
        port = request.form['port']
        comment = request.form['comment']
        if violations == 'Yes':
            b = True

        try:
            # status = Status(value=False)
            # db.session.add(status)
            # db.session.commit()
            # print(status)
            statuss = Status.query.all()  # Извлекаем всех пользователей
            for st in statuss:
                print(st.id, st.value)
            status = Status.session.get(1)
            print(status)
            if status:
                new_address = Address(ip=ip, comments=comment )
                db.session.add(new_address)
                db.session.commit()
            return render_template("addIP.html")
        except:
            return 'щось ввели не те'
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
