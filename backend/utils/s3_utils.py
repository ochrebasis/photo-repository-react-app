import boto3

def initialize_s3_client(region: str):
    """Initialize the S3 client."""
    return boto3.client('s3', region_name=region)

def upload_to_s3(s3_client, bucket_name: str, file, filename: str) -> str:
    """
    Upload a file to S3.

    Args:
        s3_client: Initialized S3 client.
        bucket_name: Name of the S3 bucket.
        file: File object to upload.
        filename: Target filename in S3.

    Returns:
        str: Public URL of the uploaded file.
    """
    s3_client.upload_fileobj(file, bucket_name, filename, ExtraArgs={'ACL': 'public-read'})
    return f"https://{bucket_name}.s3.{s3_client.meta.region_name}.amazonaws.com/{filename}"

def list_s3_objects(s3_client, bucket_name: str):
    """
    List all objects in an S3 bucket.

    Args:
        s3_client: Initialized S3 client.
        bucket_name: Name of the S3 bucket.

    Returns:
        list[dict]: List of objects with their keys and public URLs.
    """
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    return [
        {
            'filename': item['Key'],
            'url': f"https://{bucket_name}.s3.{s3_client.meta.region_name}.amazonaws.com/{item['Key']}"
        }
        for item in response.get('Contents', [])
    ]
