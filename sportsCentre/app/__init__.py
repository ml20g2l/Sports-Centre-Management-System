# A file to make python treat directories containing the file as packages

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#define datetime
import datetime

db = SQLAlchemy()
# from config import config

def create_app():
  # to allocate instance of Flask into app  
  app = Flask(__name__)
  # to laod this configuration into app 
  # app.secret_key = 'LOVE'
  app.config.from_object('config')
  app.jinja_env.globals.update(datetime=datetime)
  # app.config.from_object(config[config_name])
  # config[config_name].init_app(app)

  
  # the blueprint object 'main' made in main.__init__.py is registered (blueprint registeration) 
  from app.main import main as main_bp
  app.register_blueprint(main_bp)
  # the blueprint object 'auth' registration 
  from app.auth import auth as auth_bp
  app.register_blueprint(auth_bp)

  db.init_app(app)  
  return app

# Creating the app at the module level

app = create_app()

if __name__ == "__main__":

  app.run(debug=True)
