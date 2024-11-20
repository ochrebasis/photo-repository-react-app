import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from utils.sqlite_utils import initialize_db, save_photo_to_db, list_photos_from_db

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}  # Allowed file extensions
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
initialize_db()  # Initialize the database when the app starts
CORS(app)  # Enable CORS for all routes

def allowed_file(filename):
    """Check if a file is an allowed image type."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve uploaded files
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo file provided'}), 400

    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(photo.filename):
        return jsonify({'error': 'Invalid file type. Only .jpg, .jpeg, .png, .gif are allowed.'}), 400


    # Secure the filename and save locally
    filename = secure_filename(photo.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    photo.save(file_path)

    try:
        # Save metadata to the database
        photo_id = save_photo_to_db(filename, file_path)
        return jsonify({'message': 'Photo uploaded successfully', 'id': photo_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/photos', methods=['GET'])
def list_photos():
    try:
        photos = list_photos_from_db()
        # Add full URL for file_path
        for photo in photos:
            photo['url'] = f"http://127.0.0.1:5000/uploads/{photo['filename']}"
        return jsonify({'photos': photos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
