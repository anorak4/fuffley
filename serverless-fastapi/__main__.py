"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import iam
import json

region = aws.config.region

custom_stage_name = 'serverless-fastapi-'

##################
## S3 bucket
##################

# Create an S3 bucket to save lambda deployment package.

serverless_fastapi_kms = aws.kms.Key("serverless-fastapi-kms",
    description="KMS key 1",
    deletion_window_in_days=7)
serverless_fastapi_bucket = aws.s3.Bucket("serverless-fastapi-bucket", acl="private")
serverless_fastapi_bucket_object = aws.s3.BucketObject("serverless-fastapi-bucketObject",
    key="someobject",
    bucket=serverless_fastapi_bucket.id,
    source=pulumi.FileAsset("api/serverless_fastapi_deployment_package.zip"),
    kms_key_id=serverless_fastapi_kms.arn)

##################
## Lambda Function
##################

# Create a Lambda function, using code from the `./app` folder.

serverless_fastapi_lambda_func = aws.lambda_.Function("serverless-fastapi-lambda",
    role=iam.lambda_role.arn,
    runtime="python3.8",
    handler="main.handler",
    s3_bucket=serverless_fastapi_bucket.id,
    s3_key="someobject",
    s3_object_version=serverless_fastapi_bucket_object.version_id    
    )