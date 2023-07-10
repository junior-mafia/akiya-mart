import os
import requests

GOOGLE_MAPS_API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]


# DANGER THIS FUNCTION COSTS MONEY
# 1/3 OF ALL LISTINGS ARE MISSING?
def gelocate(address):
    params = {"address": address, "key": GOOGLE_MAPS_API_KEY}
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    response = requests.get(url, params=params)
    json = response.json()
    results = json.get("results")
    if results is not None:
        if len(results) > 0:
            first_result = results[0]
            location = first_result["geometry"]["location"]
            lat = location["lat"]
            lon = location["lng"]
            return {"lat": lat, "lon": lon, "is_geocoded": True}
        else:
            return {"lat": None, "lon": None, "is_geocoded": True}
    else:
        return {"lat": None, "lon": None, "is_geocoded": True}
