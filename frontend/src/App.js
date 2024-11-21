import React, { useState, useEffect } from 'react';
import { ReactComponent as Logo } from './logo.svg';
import axios from 'axios';
import './App.css';

const App = () => {
  const [photos, setPhotos] = useState([]); // Store photo URLs
  const [selectedFile, setSelectedFile] = useState(null); // Selected file for upload
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(''); // Error message
  const [lightbox, setLightbox] = useState({ isOpen: false, photo: null, style: {} }); // Lightbox state
  const [storageStats, setStorageStats] = useState({ total: 0, remaining: 0, max: 0 });
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
  const MAX_FILE_SIZE = 35 * 1024 * 1024; // 35MB in bytes

  // Fetch photos from the backend
  useEffect(() => {
    const fetchPhotos = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/photos`);
        setPhotos(response.data.photos);
      } catch (err) {
        console.error('Error fetching photos:', err);
        setError('Failed to fetch photos');
      }
    };

    const fetchStorageStats = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/storage-stats`);
        setStorageStats({
          total: response.data.total_storage,
          remaining: response.data.remaining_storage,
          max: response.data.max_storage
        });
      } catch (err) {
        console.error('Error fetching storage stats:', err);
      }
    };
    
    fetchStorageStats();
    fetchPhotos();
  }, []);

  // Helper to convert bytes to gigabytes
  const bytesToGigabytes = (bytes) => (bytes / (1024 * 1024 * 1024)).toFixed(2);
  const storagePercentage = (storageStats.total / storageStats.max) * 100;

  // Handle file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file.size > MAX_FILE_SIZE) {
      setError('File size exceeds the 35MB limit');
      setSelectedFile(null); // Clear the selection
      return;
    }
    setSelectedFile(file);
    setError(''); // Clear any previous errors
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file to upload');
      return;
    }
    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('photo', selectedFile);

    try {
      await axios.post(`${BACKEND_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const updatedPhotos = await axios.get(`${BACKEND_URL}/photos`);
      setPhotos(updatedPhotos.data.photos);
    } catch (err) {
      console.error('Error uploading photo:', err);
      setError(`Failed to upload photo: ${err.response?.data?.error || err.message}`);
    } finally {
      setLoading(false);
      setSelectedFile(null);
    }
  };

  // Open the lightbox and calculate the image dimensions
  const openLightbox = (photo) => {
    const img = new Image();
    img.src = photo.url;

    img.onload = () => {
      const { naturalWidth, naturalHeight } = img;
      const viewportWidth = window.innerWidth;
      const viewportHeight = window.innerHeight;

      const widthRatio = viewportWidth / naturalWidth;
      const heightRatio = viewportHeight / naturalHeight;

      // Scale the image based on the smaller ratio to ensure it fits
      const scale = Math.min(widthRatio, heightRatio);

      setLightbox({
        isOpen: true,
        photo,
        style: {
          width: `${naturalWidth * scale}px`,
          height: `${naturalHeight * scale}px`,
        },
      });
    };
  };

  // Close the lightbox
  const closeLightbox = () => {
    setLightbox({ isOpen: false, photo: null, style: {} });
  };

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <Logo className='header-icon'/>
          <h1>Photo Repository</h1>
        </header>
        <p>Hello! Welcome to my photo repository. If correctly deployed this server is using an <b>EC2 instance</b>, <b>S3 bucket</b> and <b>VPC</b> within AWS services to deliver you these images.</p>
        <p>Feel free to upload, if you'd like! Be mindful of what you decide to upload and how large the images sizes are!</p>
        {/* Storage Usage Progress Bar */}
        <div className="storage-progress">
          <div className="progress-bar">
            <div
              className="progress"
              style={{ width: `${storagePercentage}%` }}
            >
            </div>
            <span className="progress-text">
              Storage Usage: {bytesToGigabytes(storageStats.total)}GB / {bytesToGigabytes(storageStats.max)}GB
            </span>
          </div>
        </div>
        {/* File Upload Form */}
        <div className="upload-form">
          <h2>Upload Photo</h2>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleUpload} disabled={loading}>
            {loading ? 'Uploading...' : 'Upload'}
          </button>
          {error && <p className="error-message">{error}</p>}
        </div>

        {/* Photo Gallery */}
        <div className="gallery">
          <h2>Photo Gallery</h2>
          {photos.length > 0 ? (
            <div className="photo-grid">
              {photos.map((photo) => (
                <div className="photo-wrapper">
                  <img
                    key={photo.id}
                    src={photo.url}
                    alt={photo.filename}
                    onClick={() => openLightbox(photo)} // Open lightbox on click
                  />
                </div>
              ))}
            </div>
          ) : (
            <p className="empty-gallery">No photos uploaded yet.</p>
          )}
        </div>
      </div>

      {/* Lightbox */}
      {lightbox.isOpen && (
        <div className="lightbox" onClick={closeLightbox}>
          <div className="lightbox-content" onClick={(e) => e.stopPropagation()}>
            <img
              src={lightbox.photo.url}
              alt={lightbox.photo.filename}
              style={lightbox.style} // Dynamically apply the calculated styles
            />
            <button className="close-button" onClick={closeLightbox}>
              &times;
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
