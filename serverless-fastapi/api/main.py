from fastapi import FastAPI, Request
from v1.routers import router
from mangum import Mangum
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI(title='Fuffley API',
              description='The next generation serverless API')
app.include_router(router, prefix="/v1")

templates = Jinja2Templates(directory="website")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})
    # return {"Hello Medium Reader": "from FastAPI & API Gateway"}


# to make it work with Amazon Lambda, we create a handler object
handler = Mangum(app=app)
