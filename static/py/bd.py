# from datetime import datetime
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flsite import db, Status
#
#
#
# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ip = db.Column(db.String(25), nullable=False, unique=True)
#     update = db.Column(db.DateTime, default=datetime.utcnow)
#     created = db.Column(db.DateTime, nullable=True)
#     comments = db.Column(db.Text, nullable=True)
#     checked = db.Column(db.Boolean, nullable=True)
#     id_svmap = db.relationship('Svmap', backref='address', uselist=False)  # Связь с профилем пользователя   1:1
#     id_nmap = db.relationship('Nmap', backref='address', uselist=False)  # Связь с профилем пользователя   1:1         1:m
#     id_status = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)    # m:1
#     def __repr__(self):
#         return f'<Address {self.id_svmap}>'
#
#
# class Svmap(db.Model):
#     __tablename__ = 'svmap'
#     id = db.Column(db.Integer, primary_key=True)
#     ports = db.Column(db.String(255), nullable=True)
#     version = db.Column(db.String(50), nullable=True)
#     dev_name = db.Column(db.String(50), nullable=True)
#     id_address = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True, nullable=False)
#
#     def __repr__(self):
#         return f'<Ports {self.ports}>'
#
#
# class Nmap(db.Model):
#     __tablename__ = 'nmap'
#     id = db.Column(db.Integer, primary_key=True)
#     other = db.Column(db.String(255), nullable=True)
#     id_address = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True, nullable=False)
#
#     def __repr__(self):
#         return f'<Other {self.id_address}>'
#
#
# class Status(db.Model):      # 1:m
#     __tablename__ = 'status'
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Boolean, nullable=True)
#     id_address = db.relationship('Address', backref='status', lazy=True)  # Связь с постами пользователя
#
#     def __repr__(self):
#         return f'<Value {self.value}>'
#
#
# # перевіряє чи створені два значення True False в таблиці Status
# def crStatusTF():
#     nstatus = Status.query.all()
#     if len(nstatus) == 0:
#         status_tr = Status(value=True)
#         status_fl = Status(value=False)
#         db.session.add(status_tr)
#         db.session.add(status_fl)
#         db.session.commit()
#
# # if __name__ == '__main__':
# #     app = Flask(__name__)
# #     # app.config['SQLALCHEMY_DATABASE_URI'] = 's'
# #     app.config['SECRET_KEY'] = 'hard to guess string'
# #     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbscan.db'
# #     db = SQLAlchemy(app)