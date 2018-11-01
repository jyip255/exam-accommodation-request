from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cas import CAS

app = Flask(__name__)
cas = CAS(app, '/cas')
app.config['CAS_SERVER'] = 'https://login.uconn.edu'
#app.config['CAS_AFTER_LOGIN'] = 'route_root'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)
from app import views, models
