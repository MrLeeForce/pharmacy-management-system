# init_db.py
from app import create_app
from models import db, User, Product
from utils import load_initial_data

app = create_app()

with app.app_context():
    # Delete existing database file if it exists
    import os
    if os.path.exists('data/pharmacy.db'):
        os.remove('data/pharmacy.db')
    
    # Create fresh tables
    db.create_all()
    
    # Create admin user
    admin = User(username="M", pharmacy_code="M1")
    admin.set_password("M")
    db.session.add(admin)
    
    # Load products
    load_initial_data()
    db.session.commit()
    
    print("✅ Database initialized successfully!")
    print(f"Admin user created: username=M, pharmacy_code=M1, password=M")