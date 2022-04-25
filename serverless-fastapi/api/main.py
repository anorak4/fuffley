from fastapi import FastAPI, Request
from v1.routers import router
from mangum import Mangum
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title='Fuffley API',
              description='The next generation serverless API',
              openapi_prefix=openapi_prefix)

app.include_router(router, prefix="/v1")

templates = Jinja2Templates(directory="website")

@app.get("/website", response_class=HTMLResponse)
async def read_website(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})
    # return {"Hello Medium Reader": "from FastAPI & API Gateway"}

@app.get("/")
async def read_hello():
    print("Calling read_hello method")
    return {"message": "World"}


# to make it work with Amazon Lambda, we create a handler object
print("Calling Mangum handler")
handler = Mangum(app=app)
