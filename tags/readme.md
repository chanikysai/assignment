# EC2 Tag Updater Script

## Overview
This Python script updates tags for AWS EC2 instances based on data provided in CSV and text files. It uses the boto3 library to interact with AWS services.

## Requirements
- Python 3.x
- boto3 library (`pip install boto3`)

## Setup
1. **AWS Credentials**: Ensure you have AWS credentials (access key and secret key) with permissions for EC2 tag updates.
2. **Files Needed**:
   - `instance_ids.txt`: Contains instance IDs (one per line).
   - `tags_details.csv`: CSV file with columns 'Instance ID', 'Hostname', 'Department', and 'New Department'.

## Usage
1. **Update AWS Credentials**: Replace `access_key` and `secret_key` variables with your AWS IAM credentials.
2. **Specify Region**: Modify the `region` variable to match your AWS region.
3. **Run the Script**:
   ```bash
   python update_ec2_tags.py
