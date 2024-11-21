from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from utils.s3_utils import initialize_s3_client, upload_to_s3, list_s3_objects
import uuid
import os

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],  # Global limits
)

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})  # Enable CORS for all routes

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION')  # Replace with your AWS region
S3_BUCKET = os.getenv('S3_BUCKET')  # Replace with your S3 bucket name

# Allowed extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Initialize S3 client
s3_client = initialize_s3_client(AWS_REGION)

def allowed_file(filename):
    """Check if a file is an allowed image type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@limiter.limit("45 per hour")  # Custom limit for this endpoint
def upload_photo():
    MAX_FILE_SIZE = 35 * 1024 * 1024 # 35MB in bytes
    MAX_STORAGE = 10 * 1024 * 1024 * 1024 # 10GB in bytes

    if 'photo' not in request.files:
        return jsonify({'error': 'No photo file provided'}), 400

    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(photo.filename):
        return jsonify({'error': 'Invalid file type. Only .jpg, .jpeg, .png, .gif are allowed.'}), 400
    
    # Check file size
    photo.stream.seek(0, os.SEEK_END)  # Move the stream position to the end
    file_size = photo.stream.tell()   # Get the current stream position as the size
    photo.stream.seek(0)              # Reset the stream position to the beginning

    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds the 35MB limit'}), 413

    total_storage_used = sum(obj['Size'] for obj in list_s3_objects(s3_client, S3_BUCKET))
    if total_storage_used + file_size > MAX_STORAGE:
        return jsonify({'error': 'Storage limit reached. Cannot upload more photos.'}), 403

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4()}-{photo.filename}"

    try:
        # Upload to S3 using the utility function
        photo_url = upload_to_s3(s3_client, S3_BUCKET, photo, unique_filename)
        return jsonify({'message': 'Photo uploaded successfully', 'photo_url': photo_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/photos', methods=['GET'])
def list_photos():
    try:
        # List photos from S3 using the utility function
        photos = list_s3_objects(s3_client, S3_BUCKET)
        # Add an incremental ID to each photo for React compatibility
        for idx, photo in enumerate(photos):
            photo['id'] = idx + 1
        return jsonify({'photos': photos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/storage-stats', methods=['GET'])
def get_storage_stats():
    MAX_STORAGE = 10 * 1024 * 1024 * 1024  # 10GB in bytes

    try:
        # Calculate total storage used
        total_storage_used = sum(obj['Size'] for obj in list_s3_objects(s3_client, S3_BUCKET))
        remaining_storage = MAX_STORAGE - total_storage_used

        return jsonify({
            'total_storage': total_storage_used,
            'remaining_storage': remaining_storage,
            'max_storage': MAX_STORAGE
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
