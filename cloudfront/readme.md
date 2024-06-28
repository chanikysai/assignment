Setting Up CloudFront Distribution for Secure Access to S3 Files
This guide outlines the steps to configure a CloudFront distribution to securely serve public and private files from an AWS S3 bucket (acme-downloads), while meeting specific access control and security requirements.

Step-by-Step Instructions
1. Configure S3 Bucket
Create an S3 bucket named acme-downloads.

Inside the bucket, create two folders:

public
private
2. Create IAM Policy for CloudFront Access
Create an IAM policy allowing CloudFront to access objects in the acme-downloads bucket. Use the example policy below:

{
    "Version": "2012-10-17",
    "Statement": {
        "Sid": "AllowCloudFrontServicePrincipalReadOnly",
        "Effect": "Allow",
        "Principal": {
            "Service": "cloudfront.amazonaws.com"
        },
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::acme-downloads/*",
        "Condition": {
            "StringEquals": {
                "AWS:SourceArn": "arn:aws:cloudfront::111122223333:distribution/<CloudFront distribution ID>"
            }
        }
    }
}



Attach this policy to the S3 bucket acme-downloads.

3. Create CloudFront Distribution
Go to the CloudFront console and create a new distribution.

Set the S3 bucket acme-downloads as the origin.

Configure the distribution settings:

Enable HTTPS for secure access.
Redirect HTTP to HTTPS.
4. Configure Access Control
Public Folder Access
Configure the public folder to allow public access via the CloudFront distribution.
Private Folder Access
Block public access to the private folder by default.

Create two IAM users, Rob and Mark, and grant them S3 access permissions.

Use pre-signed URLs to grant temporary access to specific files in the private folder. Rob and Mark can generate these URLs to share access to private files.

5. Enable Logging
Create an S3 bucket named acme-downloads-logs to store CloudFront access logs.

Configure CloudFront to log all access requests to this bucket.

6. Test the Configuration
Upload a sample file (sample.html) to both the public and private folders.

Verify that the file in the public folder is accessible through the CloudFront URL.

Generate a pre-signed URL for the file in the private folder and verify that it is accessible only through this URL.

7. Maintain and Monitor
Regularly review access logs stored in acme-downloads-logs to monitor access patterns and detect any unauthorized access attempts.

Periodically update IAM policies and CloudFront settings to adhere to the best security practices.

Example Commands and Scripts
Create IAM Policy
bash
Copy code
aws iam create-policy --policy-name AllowCloudFrontAccess --policy-document file://cloudfront-access-policy.json
Create Pre-signed URL
python
Copy code
import boto3
from botocore.exceptions import NoCredentialsError

s3_client = boto3.client('s3')

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name, 'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        print("Credentials not available.")
        return None

    return response

# Example usage
url = generate_presigned_url('acme-downloads', 'private/sample.html')
print(url)
Conclusion
By following these steps, you can securely serve public and private files from your S3 bucket using CloudFront, ensuring that access is controlled and logged appropriately. This setup allows for flexible access management with pre-signed URLs and helps maintain security and compliance with access logging.