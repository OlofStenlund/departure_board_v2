import requests
from dotenv import load_dotenv
import os
import pandas as pd


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
        try:
            if (f'{stop}, {municipality}') in i['name']:
                gid = i['gid']
            return gid
        except KeyError as ke:
            raise KeyError("Invalid input: GID could not be found for that stop") from ke




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


def prepare_departures_data(data: list, limit: int) -> list:
    deps_list = []
    for i in range(0, limit):
        sj = data[i]['serviceJourney']
        direction = sj["direction"]
        destination = sj["directionDetails"]["shortDirection"]
        short_name = sj["line"]["shortName"]
        mode = sj["line"]["transportMode"]
        wheelchair_acc = sj["line"]["isWheelchairAccessible"]

        planned_departure = pd.to_datetime(data[i]["plannedTime"])
        est_departure = pd.to_datetime(data[i]["estimatedOtherwisePlannedTime"])
        cancelled = data[i]["isCancelled"]

        deps_list.append(
            {'Direction': direction, 
            'Destination': destination, 
            'Short_name': short_name,
            'Mode': mode,
            'Wheelchair_acc': wheelchair_acc,
            'Planned_departure': planned_departure,
            'Est_departure': est_departure,
            'Cancelled': cancelled}
            )
    
    return deps_list
