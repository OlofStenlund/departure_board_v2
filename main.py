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

stop = "Brunnsbotorget"
### Since some env-variables are loaded in dependancies, we reset the env-variables first thing.
### This is because the TOKEN needs to be checked and updated

def main():
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
    limit = 10
    api_url = "https://ext-api.vasttrafik.se/pr/v4"
    request_headers = {"Authorization": f"Bearer {TOKEN}"}

    decoded_token = decode_token(TOKEN)
    expiry_seconds = get_token_expiry(decoded_token)


    # Update token if needed
    if not check_token_validity(expiry_seconds=expiry_seconds):
        print(check_token_validity(expiry_seconds=expiry_seconds))
        print("Token not valid")
        generate_new_token(env_path, TOKEN_GENERATION_BASE_URL, TOKEN_GENERATION_HEADERS)
        # reload_env(env_path) # In case of new token, don't forget to reload envs
    if check_token_validity(expiry_seconds=expiry_seconds):
        # print(check_token_validity(expiry_seconds=expiry_seconds))
        print("Token valid")
    
    # Reaload envs
    reload_env(env_path=env_path)
    TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
    TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
    TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
    SECRET = os.getenv("SECRET")
    TOKEN = os.getenv("TOKEN")


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
    
    prep_data = prepare_departures_data(data, limit)
    
    def get_current_times(now):
        current_week= now.isocalendar()[1]
        current_day = now.day
        current_year = now.year
        current_month = now.month
        current_hour = now.hour

        if current_hour < 10:
            current_hour = f"0{current_hour}"
        current_minute = now.minute
        if current_minute < 10:
            current_minute = f"0{current_minute}"

        current_day_name = now.strftime("%A")
        current_month_name = now.strftime("%B")
        current_time = {
            "year": current_year, 
            "month_no": current_month, 
            "month_name": current_month_name, 
            "week": current_week, 
            "day_no": current_day, 
            "day_name": current_day_name, 
            "hour": current_hour, 
            "minute": current_minute
            }
        return current_time

    times = get_current_times(datetime.now())

    return prep_data, times
