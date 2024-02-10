import python_jwt as jwt
import requests
import pandas as pd
from datetime import datetime, time, timedelta
import time
from main_functions import generate_connetion_url, generate_token, read_token, get_token_expiry, get_gid, get_departures_list, get_current_times
from connection_details import connection_base_url

stop = "BRUNNSBOTORGET"
limit = 15

connection_url = generate_connetion_url(stop, limit)

# Anatomy of main():
# 1: Generate token if not exists
# 2: Get time for token validity. If <= 3 sec, get new token
# 3: Get GID byr sendina  request bearing bearer_token and connection_header
# 4: Get departuers based on GID (station ID)
# 5: 

def main():
    now = pd.to_datetime(datetime.now())
    
    token = read_token()
    if not token:
        token = generate_token()
    exp = get_token_expiry(token)
    valid_time = (exp - now).total_seconds()
    
    if valid_time <= 3:
        print("New token needed. Stand by...")
        time.sleep(4)
        token = generate_token()
    elif valid_time > 3:
        pass
    else: 
        ValueError

    # Adapt script to token
    bearer_token = f'Bearer {token}'
    connection_headers = {f'Authorization': bearer_token}

    # Fetch the actual departures:
    gid = get_gid(connection_base_url, connection_url, connection_headers)
    get_departures_url = f"/stop-areas/{gid}/departures?limit=10"
    departures_response = requests.get(f"{connection_base_url}{get_departures_url}", headers=connection_headers)
    departures_data = departures_response.json()
    departures = get_departures_list(departures_data, now)
    current_time = get_current_times(now)
    return departures, current_time

    
main()
