import boto3
import csv

# Specify AWS credentials directly
access_key = ''
secret_key = ''

# Specify the AWS region you want to operate in
region = 'us-east-1'  # Replace with your desired AWS region

# Initialize Boto3 client for EC2 with specific credentials and region
session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region
)
ec2_client = session.client('ec2')

# Function to update tags for an instance
def update_tags(instance_id, hostname, old_department, new_department):
    new_tags = [{'Key': 'Department', 'Value': new_department}]
    response = ec2_client.create_tags(
        Resources=[instance_id],
        Tags=new_tags
    )
    print(f"Tags updated for instance {instance_id} (Hostname: {hostname})")

# Read instance IDs from instance_ids.txt and update tags accordingly
def update_tags_from_instance_ids(instance_ids_file, tag_details_file):
    with open(instance_ids_file, mode='r') as id_file:
        instance_ids = id_file.read().strip().splitlines()

    with open(tag_details_file, mode='r') as tag_file:
        reader = csv.DictReader(tag_file)
        for row in reader:
            instance_id = row.get('Instance ID', '').strip()
            if instance_id in instance_ids:
                hostname = row.get('Hostname', '').strip()
                old_department = row.get('Department', '').strip()
                new_department = row.get('New Department', '').strip()
                update_tags(instance_id, hostname, old_department, new_department)

# Example usage
if __name__ == "__main__":
    instance_ids_file = 'instance_ids.txt'
    tag_details_file = 'tags_details.csv'
    update_tags_from_instance_ids(instance_ids_file, tag_details_file)
