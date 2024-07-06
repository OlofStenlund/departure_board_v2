import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN_GENERATION_BASE_URL = os.getenv("TOKEN_GENERATION_BASE_URL")
TOKEN_GENERATION_HEADERS_STR = os.getenv("TOKEN_GENERATION_HEADERS")
TOKEN_GENERATION_HEADERS = json.loads(TOKEN_GENERATION_HEADERS_STR)
SECRET = os.getenv("SECRET")
TOKEN = os.getenv("TOKEN")



connection_base_url = "https://ext-api.vasttrafik.se/pr/v4"
headers = {"Authorization": f"Bearer {TOKEN}"}




def get_gid(base_url, url, headers):
    resp = requests.get(f"{base_url}{url}", headers=headers)
    data = resp.json()
    gid = data['results'][0]['gid']
    return gid

def get_departures_data(gid, limit):
    get_departures_url = f"/stop-areas/{gid}/departures?limit={limit}"
    departures_response = requests.get(
        f"{connection_base_url}{get_departures_url}", 
        headers=headers
        )
    res = departures_response.json()['results']
    return res
