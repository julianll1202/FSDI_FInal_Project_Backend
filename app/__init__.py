from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import LoginManager

naming_convention = {
    "fk":
    "fk_%(table_name)s_%(column_0_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
if __name__ == "__main__":
    app = Flask(__name__, static_folder="static", static_url_path="/")
# app = Flask(__name__, static_folder="static", static_url_path="/")
app.config.from_object(Config)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app,db, render_as_batch=True)

login = LoginManager(app)
login.login_view = 'login'
from app import routes, models