pip install --target ./package -r requirements.txt
cd package
export PATH=$PATH:"C:\Program Files\7-Zip"
7z a ../serverless_fastapi_deployment_package.zip .
cd ..
7z a serverless_fastapi_deployment_package.zip .
# TODO: add cleanup