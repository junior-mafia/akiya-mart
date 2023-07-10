from app.tasks.repo import select_listings_for_geojson
import os
import json
import requests
from random import sample
from datetime import date, datetime

BUNNYCDN_API_PASSWORD = os.environ["BUNNYCDN_API_PASSWORD"]
ENVIRONMENT = os.environ["ENVIRONMENT"]
OPEN_EXCHANGE_RATES_API_KEY = os.environ["OPEN_EXCHANGE_RATES_API_KEY"]


def complex_handler(obj):
    if isinstance(obj, datetime):
        return int(obj.timestamp())
    elif isinstance(obj, date):
        return int(datetime(obj.year, obj.month, obj.day).timestamp())
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def get_yen_per_usd():
    url = "https://openexchangerates.org/api/latest.json"
    base_currency = "JPY"
    params = {"app_id": OPEN_EXCHANGE_RATES_API_KEY, "symbols": base_currency}
    response = requests.get(url, params=params)
    return response.json()["rates"]["JPY"]


def row_to_feature(row, yen_per_usd):
    properties = {key: value for key, value in row.items()}
    properties["price_usd"] = int(row["price_yen"] / yen_per_usd)
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["lon"], row["lat"]],
        },
        "properties": properties,
    }


def lite_row_to_feature(row, yen_per_usd):
    properties = {}
    properties["bukken_id"] = row["bukken_id"]
    properties["source"] = row["source"]
    properties["price_usd"] = int(row["price_yen"] / yen_per_usd)
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["lon"], row["lat"]],
        },
        "properties": properties,
    }


def generate_geojson(listings, yen_per_usd):
    geojson = {
        "type": "FeatureCollection",
        "features": [row_to_feature(row, yen_per_usd) for row in listings],
    }
    return json.dumps(geojson, default=complex_handler)


def lite_generate_geojson(listings, yen_per_usd):
    geojson = {
        "type": "FeatureCollection",
        "features": [lite_row_to_feature(row, yen_per_usd) for row in listings],
    }
    return json.dumps(geojson, default=complex_handler)


def upload_geojson_to_wasabi(storage_zone_name, file_name, geojson_content):
    upload_url = f"https://ny.storage.bunnycdn.com/{storage_zone_name}/{file_name}"
    headers = {"AccessKey": BUNNYCDN_API_PASSWORD, "Content-Type": "application/json"}
    r = requests.put(upload_url, headers=headers, data=geojson_content)
    if r.status_code == 201:
        print(
            "AKIYA-MART-TASKS: generate-geojson: File uploaded successfully {file_name}".format(
                file_name=file_name
            )
        )
    else:
        print(
            "AKIYA-MART-TASKS: generate-geojson: Failed to upload file {file_name}, status code:".format(
                file_name=file_name
            ),
            r.status_code,
        )


def purge_cache(pull_zone_id, file_name):
    purge_cache_url = f"https://bunnycdn.com/api/pullzone/{pull_zone_id}/purgeCache"
    headers = {"AccessKey": BUNNYCDN_API_PASSWORD, "Content-Type": "application/json"}
    data = {"urls": [file_name]}
    r = requests.post(purge_cache_url, headers=headers, json=data)
    if r.status_code == 200:
        print(
            "AKIYA-MART-TASKS: generate-geojson: Cache purged successfully {file_name}".format(
                file_name=file_name
            )
        )
    else:
        print(
            "AKIYA-MART-TASKS: generate-geojson: Failed to purge cache {file_name}, status code".format(
                file_name=file_name
            ),
            r.status_code,
        )


def sample_listings(listings, size):
    sampled_list = sample(listings, size)
    return sampled_list


def geojson_task(session):
    storage_zone_name = "akiya-mart-tasks"
    pull_zone_id = "akiya-mart-tasks"
    if ENVIRONMENT == "PROD":
        file_name = "listings.geojson"
        free_filename = "listings-free.geojson"

        lite_file_name = "lite-listings.geojson"
        lite_free_filename = "lite-listings-free.geojson"
    else:
        file_name = "dev-listings.geojson"
        free_filename = "dev-listings-free.geojson"

        lite_file_name = "dev-lite-listings.geojson"
        lite_free_filename = "dev-lite-listings-free.geojson"
    listings = select_listings_for_geojson(session)
    yen_per_usd = get_yen_per_usd()

    # Paid tier
    geojson_content = generate_geojson(listings, yen_per_usd)
    upload_geojson_to_wasabi(storage_zone_name, file_name, geojson_content)

    lite_geojson_content = lite_generate_geojson(listings, yen_per_usd)
    upload_geojson_to_wasabi(storage_zone_name, lite_file_name, lite_geojson_content)
    purge_cache(pull_zone_id, file_name)

    # Free tier
    sample_size = int(len(listings) * 0.005)  # Roughly 500 listings
    free_listings = sample_listings(listings, sample_size)
    free_geojson_content = generate_geojson(free_listings, yen_per_usd)
    upload_geojson_to_wasabi(storage_zone_name, free_filename, free_geojson_content)

    free_lite_geojson_content = lite_generate_geojson(free_listings, yen_per_usd)
    upload_geojson_to_wasabi(
        storage_zone_name, lite_free_filename, free_lite_geojson_content
    )
    purge_cache(pull_zone_id, free_filename)
