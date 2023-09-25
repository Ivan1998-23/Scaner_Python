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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    update = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('Profile', backref='user', uselist=False)  # Связь с профилем пользователя   1:1
    posts = db.relationship('Post', backref='user', lazy=True)  # Связь с постами пользователя          1:m

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)  # Связь с пользователем

    def __repr__(self):
        return f'<Profile {self.full_name}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)  # Связь с пользователем

    def __repr__(self):
        return f'<Post {self.title}>'


with app.app_context():
    db.create_all()

@app.route("/home")
@app.route("/")
def index():
    user = User.query.all()

    return render_template("index.html", address=user)


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
            new_user = User(username=ip)
            db.session.add(new_user)
            db.session.commit()

            if new_user:
                new_profile = Profile(full_name=comment, user=new_user)
                db.session.add(new_profile)
                db.session.commit()
                new_post = Post(title=port, content=port, user=new_user)
                print(new_post)
                db.session.add(new_post)
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
