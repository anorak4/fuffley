"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import iam
import json

region = aws.config.region

custom_stage_name = 'serverless_fastapi_'

##################
## S3 bucket
##################

# Create an S3 bucket to save lambda deployment package.

serverless_fastapi_kms = aws.kms.Key("serverless_fastapi_kms",
    description="KMS key 1",
    deletion_window_in_days=7)
serverless_fastapi_bucket = aws.s3.Bucket("serverless_fastapi_bucket", acl="private")
serverless_fastapi_bucket_object = aws.s3.BucketObject("serverless_fastapi_bucketObject",
    key="someobject",
    bucket=serverless_fastapi_bucket.id,
    source=pulumi.FileAsset("api/serverless_fastapi_deployment_package.zip"),
    kms_key_id=serverless_fastapi_kms.arn)

##################
## Lambda Function
##################

# Create a Lambda function, using code from the `./app` folder.

serverless_fastapi_lambda_func = aws.lambda_.Function("serverless_fastapi_lambda",
    role=iam.lambda_role.arn,
    runtime="python3.7",
    handler="main.handler",
    s3_bucket=serverless_fastapi_bucket,
    s3_key=serverless_fastapi_kms,
    s3_object_version=serverless_fastapi_bucket_object    
    })
)