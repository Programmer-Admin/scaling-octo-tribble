# AWS S3 File Upload Containerized Script

## Introduction

This project provides a Python script to monitor a specified directory, zip its contents, and upload the zip file to Amazon S3. The script is containerized using Docker, allowing for easy deployment and execution in various environments.

## Features

- Monitors a directory for changes (file creation, modification, deletion).
- Zips the contents of the directory with maximum compression.
- Uploads the zip file to Amazon S3.
- Dynamically fetches AWS credentials from the AWS CLI configuration.
- Allows users to choose an AWS profile for authentication.
- Disables root access within the Docker container for enhanced security.

## Prerequisites

- Docker installed on your system.
- AWS CLI configured with profiles if required.
- Python 3.6 or higher installed locally (for script development).

## Usage

1. Clone the repository:

```bash
git clone https://github.com/your_username/your_repository.git
cd your_repository
```
2. Create a .env file and specify the environment variables:

```
MONITORED_DIRECTORY=/path/to/monitored/directory
```
3. Build the Docker image:
```bash
docker build -t aws-s3-upload-central .
```
4. Run the Docker container:
```bash
docker run --name s3-uploader --rm -d --env-file [PATH_TO_ENV_FILE_IN_HOST] s3-upload-central
```
5. Follow the on-screen instructions to select the AWS profile if prompted.

## Security Considerations

- Avoid embedding AWS credentials directly into Docker images.

- Utilize environment variables or securely mount AWS credentials at runtime.

- Follow best practices for securing AWS credentials, such as rotating them regularly.

- Monitor Docker container activities and implement logging and auditing mechanisms.

## Contributors

- Abhik Biswas
