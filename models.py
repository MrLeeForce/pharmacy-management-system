from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pharmacy_code = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    strength = db.Column(db.String(50))
    company = db.Column(db.String(100))
    salt = db.Column(db.String(100))
    uses = db.Column(db.String(100))  # pain_killer, antibiotic etc
    type = db.Column(db.String(50))   # tablet, capsule, syrup
    batch_id = db.Column(db.String(50), unique=True)
    pack_price = db.Column(db.Float)
    packs_quantity = db.Column(db.Integer)
    units_per_pack = db.Column(db.Integer)
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    @property
    def unit_price(self):
        return round(self.pack_price / self.units_per_pack, 2) if self.units_per_pack else 0