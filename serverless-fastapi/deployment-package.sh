mkdir api/package
pip install --target api/package -r api/requirements.txt
export PATH=$PATH:"C:\Program Files\7-Zip"
rm serverless_fastapi_deployment_package.zip
cd api/package
7z a ../../serverless_fastapi_deployment_package.zip .
cd ..
rm -r package
7z a ../serverless_fastapi_deployment_package.zip .
# TODO: add cleanup