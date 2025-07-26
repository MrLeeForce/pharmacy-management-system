# reset_db.py
import os
from app import create_app
from models import db, User, Product

app = create_app()

with app.app_context():
    # Remove existing database
    db_path = os.path.join(app.instance_path, 'pharmacy.db')
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create fresh database
    db.create_all()
    
    # Create admin user
    admin = User(username="M", pharmacy_code="M1")
    admin.set_password("M")
    db.session.add(admin)
    
    # Commit changes
    db.session.commit()
    print("✅ Database reset complete!")
    print("Admin user created: username=M, pharmacy_code=M1, password=M")