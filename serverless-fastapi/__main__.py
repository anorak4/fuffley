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


####################################################################
##
## API Gateway REST API (API Gateway V1 / original)
##    /{proxy+} - passes all requests through to the lambda function
##
####################################################################

my_demo_api = aws.apigateway.RestApi("myDemoAPI", description="This is my API for demonstration purposes")
my_demo_resource = aws.apigateway.Resource("proxy",
    rest_api=my_demo_api.id,
    parent_id=my_demo_api.root_resource_id,
    path_part="{PROXY+}")
my_demo_method = aws.apigateway.Method("myDemoMethod",
    opts=pulumi.ResourceOptions(depends_on=[my_demo_resource, my_demo_api]),
    rest_api=my_demo_api.id,
    resource_id=my_demo_resource.id,
    http_method="ANY",
    authorization="NONE")

# lambda_ARN=serverless_fastapi_lambda_func.invoke_arn
# print("This is ARN"+lambda_ARN)
my_demo_integration = aws.apigateway.Integration("myDemoIntegration",
    opts=pulumi.ResourceOptions(depends_on=[my_demo_resource, my_demo_api, my_demo_method, serverless_fastapi_lambda_func]),
    rest_api=my_demo_api.id,
    resource_id=my_demo_resource.id,
    http_method="ANY",
    type="AWS_PROXY",
    integration_http_method="POST",
    uri=pulumi.Output.concat("arn:aws:apigateway:us-east-2:lambda:path/2015-03-31/functions/",serverless_fastapi_lambda_func.arn,"/invocations")
#     cache_key_parameters=["method.request.path.param"],
#     cache_namespace="foobar",
#     timeout_milliseconds=29000,
#     request_parameters={
#         "integration.request.header.X-Authorization": "'static'",
#     },
#     request_templates={
#         "application/xml": """{
#    "body" : $input.json('$')
# }
# """,
#     }
)

# # Create a single Swagger spec route handler for a Lambda function.
# def swagger_route_handler(arn):
#     return ({
#         "x-amazon-apigateway-any-method": {
#             "x-amazon-apigateway-integration": {
#                 "uri": f'arn:aws:apigateway:{region}:lambda:path/2015-03-31/functions/{arn}/invocations',
#                 "passthroughBehavior": "when_no_match",
#                 "httpMethod": "POST",
                
#                 "requestParameters" : {
#                     "integration.request.querystring.input" : "method.request.querystring.input"
#                     # "integration.request.querystring.stage" : "method.request.querystring.version",
#                     # "integration.request.header.x-userid" : "method.request.header.x-user-id",
#                     # "integration.request.path.op" : "method.request.path.service"
#                 },

                                
#                 "type": "aws_proxy",
#             },
#         },
#     })

# # Create the API Gateway Rest API, using a swagger spec.
# rest_api = aws.apigateway.RestApi("api",
#     body=lambda_func.arn.apply(lambda arn: json.dumps({
#         "swagger": "2.0",
#         "info": {"title": "api", "version": "1.0"},
#         "paths": {
#             "/{proxy+}": swagger_route_handler(arn),
#         },
#     })))

# Create a deployment of the Rest API.
deployment = aws.apigateway.Deployment("api-deployment",
    opts=pulumi.ResourceOptions(depends_on=[my_demo_resource, my_demo_api, my_demo_method, my_demo_integration]),
    rest_api=my_demo_api.id,
    # Note: Set to empty to avoid creating an implicit stage, we'll create it
    # explicitly below instead.
    stage_name="",
)

# Create a stage, which is an addressable instance of the Rest API. Set it to point at the latest deployment.
stage = aws.apigateway.Stage("api-stage",
    rest_api=my_demo_api.id,
    deployment=deployment.id,
    stage_name=custom_stage_name,
)

# Give permissions from API Gateway to invoke the Lambda
invoke_permission = aws.lambda_.Permission("api-lambda-permission",
    action="lambda:invokeFunction",
    function=serverless_fastapi_lambda_func.name,
    principal="apigateway.amazonaws.com",
    source_arn=deployment.execution_arn.apply(lambda arn: arn + "*/*"),
)