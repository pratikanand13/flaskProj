import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:HDGIKwpoQTWXpsdXhNgZGsnehjvEspVT@autorack.proxy.rlwy.net:17950/railway')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-default-jwt-secret-key')
    S3_BUCKET = os.getenv('S3_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
