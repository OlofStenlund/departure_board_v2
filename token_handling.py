import jwt
import requests
import os
import json

from datetime import datetime, time, timedelta
from dotenv import load_dotenv

load_dotenv()

TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")


def decode_token(token):
    decoded_token = jwt.decode(jwt=token, options={"verify_signature": False})
    return decoded_token

def get_token_expiry(decoded_token):
    exp = decoded_token['exp']
    start = datetime(1970, 1, 1)
    token_expiry = start + timedelta(0,exp)
    now = datetime.now()
    valid_seconds = (token_expiry - now).total_seconds()
    return valid_seconds

def generate_token():
    resp = requests.post(TOKEN_GENERATION_BASE_URL, data='grant_type=client_credentials', headers = TOKEN_GENERATION_HEADERS)
    data = resp.json()
    token = data['access_token']
    return token

