import jwt
import requests
import os
import json

from time import sleep
from datetime import datetime, timedelta
from env_handling import *



def decode_token(token) -> dict:
    """
    Takes a json web token and decodes it.
    """
    decoded_token = jwt.decode(
        jwt=token, 
        options={"verify_signature": False}
        )
    return decoded_token


def get_token_expiry(decoded_token: dict) -> float:
    """
    Takes a decoded json web token in the form of a dict, 
    and extracts the validity in seconds and microseconds.
    """
    expiry_string = decoded_token['exp']
    start = datetime(1970, 1, 1)
    token_expiry = (
        start + timedelta(0, expiry_string)
        )
    now = datetime.now()
    valid_seconds = (
        (token_expiry - now).total_seconds()
        )
    return valid_seconds


def request_token(base_url: str, token_generation_headers: dict) -> str:
    """
    Requests a new token from the API using credentials stored in dotenv environment.
    Note that requesting a new token shoul ONLY be done when a valid token is no longer 
    available, as requesting new tokens too often can cause you to be blocked from using the API.
    """
    response = requests.post(
        url = base_url, 
        data='grant_type=client_credentials', 
        headers = token_generation_headers
        )
    data = response.json()
    token = data['access_token']
    return token


def check_token_validity(expiry_seconds: int | float) -> bool:
    if expiry_seconds > 3:
        return True
    elif expiry_seconds <= 3:
        return False


def generate_new_token(env_path: str,  base_url: str, headers: dict):
    """
    Awaits the current token to run out, thereafter generates a new token asn stores in the .env-file.

    env_path: path to your .env-file, usually '.env' if in the same directory
    base_url: Specifies the url to which the POST-request should be sent.
    headers: TOKEN_GENERATION_HEADERS
    """
    print("Getting new token")
    sleep(4)
    new_token = request_token(base_url=base_url, token_generation_headers=headers)
    env_vars = read_env_vars(
        env_path=env_path
        )
    set_new_token_var(
        vars = env_vars, 
        new_token = new_token
        )
    update_token_var(
        env_path = env_path,
        env_vars = env_vars
    )
    print("New token aquired")
