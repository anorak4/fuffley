from fastapi import APIRouter, Request
from typing import Optional
import requests
# from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import sys
import time
import jwt	# JWT library for python available from https://github.com/progrium/pyjwt
import uuid
import urllib
import urllib.parse
import urllib.request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="website")

@router.get("/sisensesso", response_class=HTMLResponse)
async def read_item(request: Request, return_to: str = "", hostname: str = "sample", shared_key: str = "", username: str = "sso-test-user"):
    payload = {
    "iat": int(time.time()),
    "sub": username,
    "jti": str(uuid.uuid4())
    #"exp" : int(time.time()) + 10000, #optional- expiration time
    }

    # shared_key = "0356d5471b73bf08a3f518474bedcc418366a9245b56ad2fecea9b73c5300261"
    jwt_string = jwt.encode(payload, shared_key)
    encoded_jwt = urllib.parse.quote_plus(jwt_string)	#url-encode the jwt string
    # hostname = "https://sisense.dataflix.com"
    location = hostname + "/jwt?jwt=" + encoded_jwt

    # return_to = request.GET.get('return_to')

    if return_to is not None:
        location += "&return_to=" + hostname + return_to    
    return templates.TemplateResponse("sisense.html", {'request': request, 'location': location, 'hostname': hostname})

