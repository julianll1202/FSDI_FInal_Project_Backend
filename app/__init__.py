from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

naming_convention = {
    "fk":
    "fk_%(table_name)s_%(column_0_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app,db, render_as_batch=True)

from app import routes, models