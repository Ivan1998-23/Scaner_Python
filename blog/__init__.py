from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
	app = Flask(__name__) 
	app.debug = True
	
	app.config['SECRET_KEY'] = 'JHVASJDIGi132412923JB12412'
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbscan.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 
	db.init_app(app)
	
	with app.app_context():
		if db.engine.url.drivername == 'sqlite':
			migrate.init_app(app, db, render_as_batch=True)
		else:
			migrate.init_app(app, db)
			
	return app
