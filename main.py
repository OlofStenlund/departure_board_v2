import locale
import json
import os

from datetime import datetime
from departure_requests import *
from env_handling import *
from token_handling import *



def main(stop: str, municipality: str):

    ### Since some env-variables are loaded in dependancies, we reset the env-variables first thing.
    ### This is because the TOKEN needs to be checked and updated

    env_path = '.env'
    reload_env(env_path)

    ### Now the env-variables have been reset, we import them

    TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
    TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
    TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
    TOKEN = os.getenv("TOKEN")

    # Update token if needed
    decoded_token = decode_token(TOKEN)
    expiry_seconds = get_token_expiry(decoded_token=decoded_token)
    if not check_token_validity(expiry_seconds=expiry_seconds):
        generate_new_token(
            env_path=env_path, 
            url=TOKEN_GENERATION_BASE_URL, 
            headers=TOKEN_GENERATION_HEADERS
        )

        # Reaload envs
        reload_env(env_path=env_path)
        TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
        TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
        TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
        TOKEN = os.getenv("TOKEN")
    else:
        pass
    
    ### Declare global variables

    limit = 10 # Number of departures we want to return
    api_url = "https://ext-api.vasttrafik.se/pr/v4"    
    request_headers = {"Authorization": f"Bearer {TOKEN}"}

    gid = get_gid(
        request_headers=request_headers, 
        stop=stop,
        limit=limit, 
        municipality=municipality,
        url=api_url
        ) 
    
    data = get_departures_data(
        gid=gid, 
        limit=limit, 
        url=api_url, 
        request_headers=request_headers
        )
    
    prep_data = prepare_departures_data(
        data=data, 
        )
    
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
            "month_name": current_month_name.capitalize(), 
            "week": current_week, 
            "day_no": current_day, 
            "day_name": current_day_name.capitalize(), 
            "hour": current_hour, 
            "minute": current_minute
            }
        return current_time
    
    loc = locale.getlocale()
    loc_code = loc[0]
    locale.setlocale(category=locale.LC_TIME, locale=loc_code)
    times = get_current_times(datetime.now())

    return prep_data, times
