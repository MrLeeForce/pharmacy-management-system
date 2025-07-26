import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pharmacy-secure-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/pharmacy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PHARMACY_NAME = "Anonymous Pharmacy"
    BACKGROUND_IMAGES = ['backs1.jpg', 'backs2.jpg', 'backs3.jpg', 'backs4.jpg']