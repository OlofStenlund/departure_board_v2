import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import math 

load_dotenv()

TOKEN = os.getenv("TOKEN")

def get_gid(request_headers: dict, stop: str, municipality: str, api_url: str) -> str:
    """
    Uses the name of the stop to retrieve the GID-code for the stop.
    This GID-code is used as an ID for the stop when fetching departure data.
    request_headers is a dict of the form {"Authorization": f"Bearer {TOKEN}"}.
    The api_url is the URL to which the post-request should be sent.

    request_headers: dict
    stop: str
    municupality: str
    api_url: str
    """


    gid_generation_ext_url = f"/locations/by-text?q={stop}&limit=10&offset=0"
    resp = requests.get(
        f"{api_url}{gid_generation_ext_url}", 
        headers=request_headers
        )
    data = resp.json()

    # return only stops
    actual_stops = []
    for i in range(0, len(data['results'])):
        if data['results'][i]['locationType'] == 'stoparea':
            actual_stops.append(data['results'][i])     
    for i in actual_stops:
        if (f'{stop.capitalize()}, {municipality.capitalize()}') in i['name']:
            gid = i['gid']
            print(f"GID: {gid}")
        else:
            pass
    return gid





def get_departures_data(gid: str | int, limit: int, connection_url: str, request_headers: dict) -> list:
    """
    Fetches departure data and returns all results as a list of dictionaries.
    One dictionary per departure, len = limit.
    """
    get_departures_url = f"/stop-areas/{gid}/departures?limit={limit}"
    departures_response = requests.get(
        f"{connection_url}{get_departures_url}", 
        headers=request_headers
        )
    res = departures_response.json()['results']
    return res



### The returned dictionary needs to contain;
# bus number
# direction
# planned departure
# est departure
# time until departure

# For the new stuff, the HTML-template needs to be ammended, 
# so raincheck on that.

# Time until departure needs to be calculated somehow.
# in the previous verison, a DT-object was created by extracting
# year, month, day, and so on and coverting them into INT and
# using these ints as arguments when creating the DT-object.
# Can this be done in a better way?

def prepare_departures_data(data: list, limit: int) -> list:
    deps_list = []
    now = datetime.now()
    for i in range(0, len(data)):
        sj = data[i]['serviceJourney']
        direction = sj["direction"]
        destination = sj["directionDetails"]["shortDirection"]
        short_name = sj["line"]["shortName"]
        background_colour = sj["line"]["backgroundColor"]
        border_colour = sj["line"]["borderColor"]
        text_colour = sj["line"]["foregroundColor"]
        mode = sj["line"]["transportMode"]
        wheelchair_acc = sj["line"]["isWheelchairAccessible"]
        cancelled = data[i]["isCancelled"]

        planned_departure = pd.to_datetime(data[i]["plannedTime"]).tz_localize(None)
        est_departure = pd.to_datetime(data[i]["estimatedOtherwisePlannedTime"]).tz_localize(None)
        min_until_dep = math.floor(((est_departure - now).total_seconds()/60))
        if min_until_dep < 1:
            min_until_dep = "Nu"

        deps_list.append(
            {'Short_name': short_name,
            'Direction': direction, 
            'Planned_departure_str': planned_departure.strftime("%H:%M"),
            'Est_departure_str': est_departure.strftime("%H:%M"),
            'Leaves_in': min_until_dep,
            #Following is metadata, not meant top be displayed
            "colour": background_colour,
            "text_colour": text_colour,
            "border_colour": border_colour
            # 'Planned_departure': planned_departure,
            # 'Destination': destination, 
            # 'Mode': mode,
            # 'Wheelchair_acc': wheelchair_acc,
            # 'Cancelled': cancelled
            }
            )
    
    return deps_list
