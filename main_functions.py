# General imports
import python_jwt as jwt
import requests
import pandas as pd
from datetime import datetime, time, timedelta
import time

# Intra-project imports
from account_details import token_generation_base_url, token_generation_headers

def generate_connetion_url(stop, limit):
    connection_url = f"/locations/by-text?q={stop}&limit={str(limit)}&offset=0"
    return connection_url

def save_token(token):
    with open("token.txt", "w") as file:
        file.write(token)

def read_token():
    with open("token.txt", "r") as file:
        token = file.read().strip()
        if token:
            return token

def generate_token():
    resp = requests.post(token_generation_base_url, data='grant_type=client_credentials', headers = token_generation_headers)
    data = resp.json()
    token = data['access_token']
    save_token(token)
    return token


def get_token_expiry(token):
    token = token
    decoded_token = jwt.process_jwt(token)
    expiry = decoded_token[1]['exp']-3
    start = datetime(1970, 1, 1)
    exp = start + timedelta(0,expiry)
    return exp

def get_gid(connection_base_url, connection_url, connection_headers):
    resp = requests.get(f"{connection_base_url}{connection_url}", headers=connection_headers)
    data = resp.json()
    gid = data['results'][0]['gid']
    return gid