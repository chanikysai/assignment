# CloudFront Distribution Setup for Secure S3 File Access

This repository provides a step-by-step guide to configure an AWS CloudFront distribution to securely serve public and private files from an S3 bucket (`acme-downloads`). This configuration includes access control, HTTPS enforcement, logging, and pre-signed URL generation.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [1. Configure S3 Bucket](#1-configure-s3-bucket)
  - [2. Create IAM Policy for CloudFront Access](#2-create-iam-policy-for-cloudfront-access)
  - [3. Create CloudFront Distribution](#3-create-cloudfront-distribution)
  - [4. Enable Logging](#5-enable-logging)
  - [5. Test the Configuration](#6-test-the-configuration)
  - [6. Maintain and Monitor](#7-maintain-and-monitor)
- [Conclusion](#conclusion)

## Prerequisites
- AWS account with administrative access.
- AWS CLI configured on your local machine.
- Python environment with `boto3` installed for generating pre-signed URLs.

## Setup Instructions

### 1. Configure S3 Bucket
```bash

1. Create an S3 bucket named `acme-downloads`.
2. Inside the bucket, create two folders :
   - `public`
   - `private`

```
### 2. Create IAM Policy for CloudFront Access attch in s3 bucket
```bash

1. Create a file named `cloudfront-access-policy.json` with the following content:
   ```json
   {
       "Version": "2008-10-17",
       "Id": "PolicyForCloudFrontPrivateContent",
       "Statement": [
           {
               "Sid": "AllowCloudFrontServicePrincipal",
               "Effect": "Allow",
               "Principal": {
                   "Service": "cloudfront.amazonaws.com"
               },
               "Action": "s3:GetObject",
               "Resource": "arn:aws:s3:::acme-downloads/*",
               "Condition": {
                   "StringEquals": {
                       "AWS:SourceArn": "arn:aws:cloudfront::<ACCOUNT_ID>:distribution/<DISTRIBUTION_ID>"
                   }
               }
           }
       ]
   }

Attach this policy to the S3 bucket acme-downloads.
 ```

## 3. Create CloudFront Distribution
```bash
    Go to the CloudFront console and create a new distribution.
    Set the S3 bucket acme-downloads as the origin.
    Configure the distribution settings:
    Enable HTTPS for secure access.
    Redirect HTTP to HTTPS.
```

## 4. Create IAM Users
```bash

1. Create IAM users for Rob and Mark.

2. Attach Policies for S3 and CloudFront Access
3. Create and attach a custom policy that grants full access to the acme-downloads S3 bucket and CloudFront distributions.

```

## 5. Generate a Presigned URL

Generate a presigned URL to allow  to access a private S3 object and attempt to access the content.



## 6. Enable Logging

    Create an S3 bucket named acme-downloads-logs to store CloudFront access logs.
    Configure CloudFront to log all access requests to this bucket.

## 7. Test the Configuration

    Upload a sample file (sample.html) to both the public and private folders.
    Verify that the file in the public folder is accessible through the CloudFront URL.
    Generate a pre-signed URL for the  in the private folder and verify that it is accessible only through this URL.


## 8. Maintain and Monitor
 1. access logs stored in acme-downloads-logs to monitor access patterns and detect any unauthorized access attempts.
