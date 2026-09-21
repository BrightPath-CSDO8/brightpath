from flask import Flask
from extensions import db
from database_connection import get_connection


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "creator": get_connection,
    "pool_pre_ping": True,
    "pool_recycle": 300
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    import models
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)