from flask import Flask
from extensions import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///education.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    import models
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)