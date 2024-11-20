# Photo Repository

![Photo Repository Screenshot](/imgs/photo-repo-demo.png)

![Photo Repository On-Click Screenshot](/imgs/photo-on-click-demo.png)

## About the Project

**Photo Repository** is a web application designed to demonstrate the deployment of AWS services for IT231. It provides users with a platform to upload, store, and view images. The project showcases the integration of AWS services, including:

- **React Frontend**: The web interface for users to interact with the photo repository.
- **Flask Backend**: Facilitates communication between the frontend and the AWS services.
- **S3 Bucket**: Stores uploaded images and makes them accessible for display on the website.
- **EC2 Instance**: Hosts the frontend and backend services in the cloud.
- **VPC (Virtual Private Cloud)**: Manages the network connectivity between AWS resources and ensures secure, public access to the application.

## Features

- Upload photos to the repository.
- View photos in a responsive gallery with a lightbox feature.
- Backend integration with AWS S3 for storage.
- Deployment-ready architecture for AWS using EC2 and VPC.

## Running Locally

To test the app locally in its current "dev" state, follow these instructions:

### Prerequisites

- **Node.js** (v16+): [Install Node.js](https://nodejs.org/)
- **Python** (3.8+): [Install Python](https://www.python.org/)
- **Pip**: Comes with Python, but ensure it's installed (`pip --version`).
- **Virtual Environment**: (Optional) Recommended for Python dependencies.
- **SQLite3**: You can quickly check if you have SQLite3 installed by running: `sqlite3 --version`

### Step 1: Clone the Repository

```bash
git clone https://github.com/ochrebasis/photo-repository-react-app.git
cd photo-repository
```

### Step 2: Run the Frontend (React)

1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Open your browser at <http://localhost:3000>.

### Step 3: Run the Backend (Flask)

1. Navigate to the `backend/` directory:
   ```bash
   cd ../backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python app_local.py
   ```
5. The backend will run on <http://localhost:5000>.
6. Any images uploaded to the website will be stored locally in `backend/uploads/`.
7. Photo metadata will be saved in the `backend/photo_repo.db` SQLite database.

## Deployment on AWS

To deploy this application on AWS, follow these steps:

### Prerequisites

- **AWS Account**: Sign up at [AWS](https://aws.amazon.com/).
- **AWS CLI**: Install and configure with `aws configure`.

### Step 1: Set Up the Backend (Flask)

1. **Create an EC2 Instance**:
   - Launch an EC2 instance with a publicly accessible IP.
   - Use an Ubuntu or Amazon Linux AMI.

2. **Install Dependencies**:
   SSH into the instance and install the required software:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   sudo pip3 install flask boto3
   ```

3. **Deploy the Flask App**:
   - Copy your `backend/` directory to the EC2 instance.
   - Start the app using:
     ```bash
     python3 app_aws.py
     ```

4. **Allow HTTP Traffic**:
   - Configure the security group to allow traffic on port `5000` or use a reverse proxy (e.g., Nginx) to serve the app on port `80`.

### Step 2: Set Up the Frontend (React)

1. **Build the React App**:
   - Navigate to the `frontend/` directory and run:
     ```bash
     npm run build
     ```
   - This generates a production-ready app in the `frontend/build/` folder.

2. **Deploy to EC2**:
   - Copy the `frontend/build/` folder to your EC2 instance.
   - Serve it using a web server like Nginx or Apache.

### Step 3: Configure the S3 Bucket

1. **Create an S3 Bucket**:
   - Name the bucket (e.g., `photo-repository-bucket`) and enable public access.

2. **Update the Flask Backend**:
   - Modify the Flask app to upload images to S3.
   - Use AWS SDK (Boto3) to interact with the bucket.

3. **Set Permissions**:
   - Attach an IAM role to the EC2 instance with `AmazonS3FullAccess`.