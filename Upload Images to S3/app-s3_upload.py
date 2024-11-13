import boto3
import cv2
import yaml

# Load AWS config from yaml
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)
    
s3_client = boto3.client('s3', aws_access_key_id=config['aws']['access_key'], aws_secret_access_key=config['aws']['secret_key'])

def upload_to_s3(image, filename):
    _, img_encoded = cv2.imencode('.jpg', image)
    img_bytes = img_encoded.tobytes()

    s3_client.put_object(Bucket=config['aws']['bucket_name'], Key=filename, Body=img_bytes, ContentType='image/jpeg')
    image_url = f"https://{config['aws']['bucket_name']}.s3.amazonaws.com/{filename}"
    return image_url
