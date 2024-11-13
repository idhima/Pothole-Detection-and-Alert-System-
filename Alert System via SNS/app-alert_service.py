import boto3
import yaml

# Load AWS config from yaml
with open("config/config.yaml", "r") as file:
    config = yaml.safe_load(file)
    
sns_client = boto3.client('sns', aws_access_key_id=config['aws']['access_key'], aws_secret_access_key=config['aws']['secret_key'])

def send_alert(pothole_count, image_url):
    message = f"Alert: {pothole_count} potholes detected. See details: {image_url}"
    sns_client.publish(TopicArn=config['aws']['sns_topic_arn'], Message=message)
