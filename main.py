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


### Since some env-variables are loaded in dependancies, we reset the env-variables first thing.
### This is because the TOKEN needs to be checked and updated

env_path = '.env'
reload_env(env_path)

### Now the env-variables have been reset, we import them

TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")


### Declare global variables
# Set these variables to get the GID-code for your desired stop
stop = "Brunnsbotorget"
municipality = "Göteborg"
gid_generation_ext_url = f"/locations/by-text?q={stop}&limit=1&offset=0"

# Set the variables for the departures
limit = 1
api_url = "https://ext-api.vasttrafik.se/pr/v4"
request_headers = {"Authorization": f"Bearer {TOKEN}"}


decoded_token = decode_token(TOKEN)
expiry_seconds = get_token_expiry(decoded_token)

if not check_token_validity(expiry_seconds=expiry_seconds):
    print("Token not valid")
    generate_new_token(env_path, TOKEN_GENERATION_BASE_URL, TOKEN_GENERATION_HEADERS)
    reload_env(env_path) # In case of new token, don't forget to reload envs
if check_token_validity(expiry_seconds=expiry_seconds):
    print("Token valid")




gid = get_gid(
    request_headers=request_headers, 
    stop=stop, 
    municipality=municipality,
    api_url=api_url
    ) 



data = get_departures_data(
    gid=gid, 
    limit=limit, 
    connection_url=api_url, 
    request_headers=request_headers
    )

print(data)
# Check if token is valid
# If not, get a new one






# Get departures
# limit = 2
# get_departures_url = f"/stop-areas/{gid}/departures?limit={limit}"

# print(token_validity_seconds)

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

