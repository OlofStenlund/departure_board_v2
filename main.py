from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timedelta, time
from time import sleep
import pandas as pd
import jwt

from token_handling import *
from env_handling import *
from departure_requests import *

load_dotenv()

TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")


# Global variables
env_path = '.env'
stop = "Valand"
gid_generation_ext_url = f"/locations/by-text?q={stop}&limit=1&offset=0"
gid = get_gid(base_url=connection_base_url, url=gid_generation_ext_url, headers=headers)
print(gid)




# Get departures
# limit = 2
# get_departures_url = f"/stop-areas/{gid}/departures?limit={limit}"

decoded_token = decode_token(TOKEN)
token_validity_seconds = get_token_expiry(decoded_token)
print(token_validity_seconds)

# if token_validity_seconds > 3:
#     print("valid")
    
# elif token_validity_seconds <= 3:
#     sleep(4)
#     print("invlaid")

# print(connection_url_1)


## RELOAD ENV VARS 

# def reload_env(env_path):
#     # Clear current environment variables loaded from .env
#     for key in read_env_vars(env_path).keys():
#         os.environ.pop(key, None)
#     # Load the environment variables from the .env file
#     load_dotenv(env_path)


# # Read all variables, update TOKEN to new token
# # Reload envorinment and read in the new token as TOKEN
# # Before this can be used, we need to check if the token in vaid or not. 
# # If not, get a new token and update.
# # If valid, pass
# all_vars = read_env_vars(env_path)
# updated_vars = set_new_token_var(all_vars, TOKEN)
# print(updated_vars)

# if updated_vars:
#     update_token_var(env_path, updated_vars)
# # reload_env(env_path)
# # TOKEN = os.getenv("TOKEN")
# # print(TOKEN)

