import boto3

def initialize_s3_client(region: str):
    """Initialize the S3 client."""
    return boto3.client('s3', region_name=region)

def upload_to_s3(s3_client, bucket_name: str, file, filename: str, folder: str = "") -> str:
    """
    Upload a file to S3.

    Args:
        s3_client: Initialized S3 client.
        bucket_name: Name of the S3 bucket.
        file: File object to upload.
        filename: Target filename in S3.
        folder: Optional folder prefix.

    Returns:
        str: Public URL of the uploaded file.
    """
    try:
        # Construct the full S3 key
        key = f"{folder.rstrip('/')}/{filename}" if folder else filename
        print(f"DEBUG: Uploading to S3 with key: {key}")

        # Perform the upload
        s3_client.upload_fileobj(
            Fileobj=file,
            Bucket=bucket_name,
            Key=key,
            ExtraArgs={'ACL': 'private'},
            Config=boto3.s3.transfer.TransferConfig(multipart_threshold=5 * 1024 * 1024)  # 5MB threshold
        )

        # Generate the public URL for the uploaded file
        file_url = f"https://{bucket_name}.s3.{s3_client.meta.region_name}.amazonaws.com/{key}"
        print(f"DEBUG: File uploaded successfully. URL: {file_url}")
        return file_url
    except Exception as e:
        print(f"DEBUG: Exception in upload_to_s3: {e}")
        raise

def list_s3_objects(s3_client, bucket_name: str, prefix: str = ""):
    """
    List all objects in an S3 bucket, excluding folder placeholders.
    """
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        # Safely iterate over objects and exclude folders
        if 'Contents' in response:
            return [
                {
                    'filename': item['Key'],
                    'Size': item.get('Size', 0),
                    'url': f"https://{bucket_name}.s3.{s3_client.meta.region_name}.amazonaws.com/{item['Key']}"
                }
                for item in response['Contents']
                if not item['Key'].endswith('/')  # Exclude folder placeholders
            ]
        else:
            return []  # No objects in the bucket
    except Exception as e:
        print(f"Error listing objects: {e}")
        raise
