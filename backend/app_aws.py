from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.s3_utils import initialize_s3_client, upload_to_s3, list_s3_objects
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# AWS Configuration
AWS_REGION = "us-east-1"  # Replace with your AWS region
S3_BUCKET = "your-photo-repo-bucket"  # Replace with your S3 bucket name

# Initialize S3 client
s3_client = initialize_s3_client(AWS_REGION)

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo file provided'}), 400

    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No selected file'}), 400

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
