from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Ensure email is unique
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password storage
    images = db.relationship('Image', backref='owner', lazy=True)  # One-to-many relationship with Image

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)  # Store the filename
    file_url = db.Column(db.String(255), nullable=False)  # Store the S3 URL
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp of upload
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to User
