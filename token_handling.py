import jwt
import requests

from datetime import datetime, timedelta
from env_handling import *
from time import sleep



def decode_token(token: jwt) -> dict:
    """
    Decodes json web token.
    """
    try:
        decoded_token = jwt.decode(
            jwt=token, 
            options={"verify_signature": False}
            )
        return decoded_token
    except:
        print("Token-sting not decoadable.")
        return False


def get_token_expiry(decoded_token: dict) -> float:
    """
    Takes a decoded json web token in the form of a dict, 
    and extracts the validity in seconds and microseconds.
    """
    try:
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
    except:
        return 0


def request_token(url: str, token_generation_headers: dict) -> str:
    """
    Requests a new token from the API using credentials stored in dotenv file.
    Note that requesting a new token should ONLY be done when a valid token is no longer 
    available, as requesting new tokens too often can cause you to be blocked from using the API.
    """
    response = requests.post(
        url = url, 
        data='grant_type=client_credentials', 
        headers = token_generation_headers
        )
    data = response.json()
    token = data['access_token']
    return token


def check_token_validity(expiry_seconds: int | float) -> bool:
    try:
        if expiry_seconds > 3:
            return True
        else:
            return False
    except:
        return False


def generate_new_token(
        env_path: str, 
        url: str, 
        headers: dict
        ) -> None:
    """
    Awaits the current token to run out, thereafter generates a new token asn stores in the .env-file.

    env_path: path to your .env-file, usually '.env' if in the same directory
    base_url: Specifies the url to which the POST-request should be sent.
    headers: TOKEN_GENERATION_HEADERS
    """
    print("Getting new token")
    sleep(4)
    new_token = request_token(
        url=url, 
        token_generation_headers=headers
        )
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
