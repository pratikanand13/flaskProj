from flask import Blueprint, request, jsonify
from app.models import User, Image
from app import db, bcrypt
import boto3
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('S3_REGION')
)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 400
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@main.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    user_id = get_jwt_identity()

    try:
        s3.upload_fileobj(
            file,
            os.getenv('S3_BUCKET_NAME'),
            filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('S3_REGION')}.amazonaws.com/{filename}"
    new_image = Image(user_id=user_id, filename=filename, file_url=file_url)

    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "Image uploaded successfully", "file_url": file_url}), 201

@main.route('/images', methods=['GET'])
@jwt_required()
def get_images():
    user_id = get_jwt_identity()
    images = Image.query.filter_by(user_id=user_id).all()
    image_urls = [{"filename": img.filename, "url": img.file_url} for img in images]

    return jsonify({"images": image_urls}), 200
