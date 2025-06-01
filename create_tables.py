from app import app, db  # Import your Flask app and db instance
from models import Recipe, User, Comment  # Import your models

# Create the database tables
with app.app_context():  # Ensure you're within the app context
    db.create_all()

print("Tables created successfully!")
