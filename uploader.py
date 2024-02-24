import os
import boto3
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import configparser

# Load environment variables from .env file
load_dotenv()

# Function to upload file to Amazon S3
def upload_file(file_path, bucket_name, s3_client):
    object_name = os.path.basename(file_path)
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Upload of '{object_name}' successful")
    except Exception as e:
        print(f"Upload of '{object_name}' failed: {e}")

# Function to fetch AWS profiles from AWS CLI configuration
def get_aws_profiles():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser('~/.aws/config'))  # Assuming the AWS config file is located in the default location
    return config.sections()

# Function to fetch AWS credentials from AWS CLI configuration based on selected profile
def get_aws_credentials(profile_name):
    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()
    return {
        'aws_access_key_id': credentials.access_key,
        'aws_secret_access_key': credentials.secret_key,
        'aws_session_token': credentials.token
    }

# Function to fetch AWS region from AWS CLI configuration based on selected profile
def get_aws_region(profile_name):
    session = boto3.Session(profile_name=profile_name)
    region = session.region_name
    return region

# Get environment variables
MONITORED_DIRECTORY = os.getenv('MONITORED_DIRECTORY')
S3_BUCKET_NAME = input("Enter the S3 bucket name: ")

# Get AWS profiles and allow user to choose
aws_profiles = get_aws_profiles()
print("Select an AWS profile:")
for i, profile in enumerate(aws_profiles, 1):
    print(f"{i}. {profile}")
selected_profile_index = int(input("Enter the number corresponding to the desired profile: ")) - 1
selected_profile = aws_profiles[selected_profile_index]
aws_credentials = get_aws_credentials(selected_profile)

# Get AWS region
aws_region = get_aws_region(selected_profile)

# Create an S3 client
s3_client = boto3.client('s3', region_name=aws_region, **aws_credentials)

# Event handler to monitor changes in the directory
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f'File created: {event.src_path}')
            threading.Thread(target=upload_file, args=(event.src_path, S3_BUCKET_NAME, s3_client)).start()

    def on_modified(self, event):
        if not event.is_directory:
            print(f'File modified: {event.src_path}')
            threading.Thread(target=upload_file, args=(event.src_path, S3_BUCKET_NAME, s3_client)).start()

if __name__ == "__main__":
    # Start monitoring directory for changes
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=MONITORED_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()