from backend.app import create_app
from backend.app.extensions import db

# Important:
# import models so SQLAlchemy knows about them
from database import models

app = create_app()


with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
