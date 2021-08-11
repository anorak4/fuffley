from fastapi import APIRouter
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

router = APIRouter()

@router.get("/sso")
async def read_item(return_to: str = "/"):
    payload = {
    "iat": int(time.time()),
    "sub": "sso-test-user",
    "jti": str(uuid.uuid4())
    #"exp" : int(time.time()) + 10000, #optional- expiration time
    }

    shared_key = ""
    jwt_string = jwt.encode(payload, shared_key)
    encoded_jwt = urllib.parse.quote_plus(jwt_string)	#url-encode the jwt string
    hostname = ""
    location = hostname + "/jwt?jwt=" + encoded_jwt

    # return_to = request.GET.get('return_to')

    if return_to is not None:
        location += "&return_to=" + urllib.parse.quote(hostname) + urllib.parse.quote(return_to)    
    return RedirectResponse(location)

