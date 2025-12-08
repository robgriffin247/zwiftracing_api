import os
import httpx
import json

# These constants are needed through all endpoints
ZRAPP_API_URL = os.getenv("ZRAPP_API_URL")
HEADER = {"Authorization": os.getenv("ZRAPP_API_KEY")}


# CLUB ============================================================================================
# Returns a dictionary containing club details and riders
# - e.g. get_club(20650)
# - Given a from_id, it returns riders starting from the from_id, e.g. get_club(20650, 4598636)
def get_club(id: int, from_id: int = None):
    response = httpx.get(
        url=f"{ZRAPP_API_URL}clubs/{id}/{from_id if from_id else ''}", headers=HEADER
    )
    response.raise_for_status()
    return response.json()


# EVENT ===========================================================================================
# Returns a dictionary contain event details and ordered list of riders (not like riders endpoint) in results
# - e.g. get_event(5188741)
def get_event(id: int):
    response = httpx.get(url=f"{ZRAPP_API_URL}results/{id}", headers=HEADER)
    response.raise_for_status()
    return response.json()


# Returns a dictionary with a zwiftpower set of riders in finishing order with rider data including ID, name, club, weight, height, power, times
# - e.g. get_zp_results(5188741)
def get_zp_results(id: int):
    response = httpx.get(url=f"{ZRAPP_API_URL}zp/{id}/results", headers=HEADER)
    response.raise_for_status()
    return response.json()


# RIDER(S) ========================================================================================
# Returns a dictionary of the rider details
# - e.g. get_rider(4598636)
# - Given epoch, it returns details for that time point, e.g. get_rider(4598636, 1733011200)
def get_rider(id: int, epoch: int = None):
    response = httpx.get(
        url=f"{ZRAPP_API_URL}riders/{id}/{epoch if epoch else ''}", headers=HEADER
    )
    response.raise_for_status()
    return response.json()


# Returns a list of rider-dictionaries
# - e.g. get_riders([4598636, 5574])
# - Given epoch, it returns details for that time point, e.g. get_riders([4598636, 5574], 1733011200)
def get_riders(ids: list[int], epoch: int = None):
    response = httpx.post(
        url=f"{ZRAPP_API_URL}riders/{epoch if epoch else ''}", headers=HEADER, json=ids
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":

    id = 4598636
    rider = get_rider(id)
    with open(f"extract/data/rider_{id}.json", "w") as f:
        json.dump(rider, f)
