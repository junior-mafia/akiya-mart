import scrapy
from app.tasks.undetected_request import undetected_request
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.tasks.repo import (
    select_listings_missing_details,
    select_coordinates,
    insert_listings_details,
)
from app.tasks.google_maps import gelocate
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re

WAIT_UNTIL = EC.presence_of_element_located((By.CSS_SELECTOR, "header#header"))

CHUNK_SIZE = 500


def dedupe(items):
    seen = set()
    return [
        x
        for x in items
        if not (x["bukken_id"], x["source"]) in seen
        and not seen.add((x["bukken_id"], x["source"]))
    ]


def parse_bukken_presence(driver):
    try:
        presence = driver.find_element(
            By.CSS_SELECTOR, "div#main section.unit.unitDetail"
        )
    except NoSuchElementException:
        presence = None
    return presence


def parse_price_yen(header, data):
    if header.text == "価格":
        displayed_price_yen = data.find_element(By.CSS_SELECTOR, "strong.price").text
        price_yen = undisplay_price_yen(displayed_price_yen)
        return price_yen
    else:
        return None


def parse_remarks(header, data):
    if header.get_attribute("innerHTML") == "備考":  # Text is hidden on page load
        remarks = data.get_attribute("innerHTML")  # Text is hidden on page load
        return remarks
    else:
        return None


def parse_address(header, data):
    if header.text == "所在地":
        soup = BeautifulSoup(data.get_attribute("innerHTML"), "html.parser")
        texts = [text for text in soup.stripped_strings]
        if texts[-1] == "地図":
            texts.pop()
        return "".join(texts)
    else:
        return None


def parse_construction_year(header, data):
    if header.text == "築年月":
        construction_year = undisplay_construction_year(data.text)
        return construction_year
    else:
        return None


def parse_image_urls(driver):
    image_urls = []
    imgs = driver.find_elements(
        By.CSS_SELECTOR, "div.mainPhoto ul.mainSlidePhoto li img"
    )
    for img in imgs:
        url = img.get_attribute("src")
        image_urls.append(url)
    return image_urls


def parse_upper_table_data(driver):
    price_yen = None
    address = None
    construction_year = None
    item_detail_data = driver.find_element(By.CSS_SELECTOR, "div.detailBox")
    dls = item_detail_data.find_elements(By.CSS_SELECTOR, "dl.detailList")

    for dl in dls:
        header = dl.find_element(By.CSS_SELECTOR, "dt")
        data = dl.find_element(By.CSS_SELECTOR, "dd")
        parsed_price_yen = parse_price_yen(header, data)
        if parsed_price_yen:
            price_yen = parsed_price_yen
        parsed_address = parse_address(header, data)
        if parsed_address:
            address = parsed_address
        parsed_construction_year = parse_construction_year(header, data)
        if parsed_construction_year:
            construction_year = parsed_construction_year

    return {
        "price_yen": price_yen,
        "address": address,
        "construction_year": construction_year,
    }


def parse_lower_table_data(driver):
    remarks = None
    table_rows = driver.find_elements(By.CSS_SELECTOR, "table#detailInfoTable tr")
    for row in table_rows:
        header = row.find_element(By.CSS_SELECTOR, "th")
        data = row.find_element(By.CSS_SELECTOR, "td")
        parsed_remarks = parse_remarks(header, data)
        if parsed_remarks:
            remarks = parsed_remarks

    return {
        "remarks": remarks,
    }


def get_element_text_or_none(driver, css_selector):
    try:
        return driver.find_element(By.CSS_SELECTOR, css_selector).text
    except:
        return None


def parse_description(driver):
    point = get_element_text_or_none(
        driver,
        "p.pointText strong",
    )
    if point:
        return [point]
    else:
        return []


def parse_coordinates(driver):
    try:
        map = driver.find_element(By.CSS_SELECTOR, "div#map_canvas")
        lat = map.get_attribute("data-lat")
        lon = map.get_attribute("data-lon")
        return {"lat": lat, "lon": lon, "is_geocoded": False}
    except:
        return {"lat": None, "lon": None, "is_geocoded": False}


def undisplay_price_yen(string):
    total = 0

    # Check if "億" is in the string
    oku_match = re.search(r"(\d+(?:,\d{3})*)(?=億)", string)
    if oku_match:
        amount = oku_match.group().replace(",", "")
        # Convert to float incase the value is 1.5万
        total += int(float(amount)) * 100000000

    # Check if "万" is in the string
    man_match = re.search(r"(\d+(?:,\d{3})*(\.\d+)?)(?=万)", string)
    if man_match:
        amount = man_match.group().replace(",", "")
        total += int(float(amount)) * 10000

    if total > 0:
        return total
    else:
        return None


def undisplay_construction_year(string):
    match = re.search(r"(\d{4})年", string)
    if match:
        year = match.group(1)
    else:
        year = None
    return year


class NiftyDetailsSpider(scrapy.Spider):
    name = "nifty_details"
    source = "nifty"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "app.tasks.undetected_middleware.UndetectedMiddleware": 543,
        },
        "LOG_LEVEL": "INFO",
        "DISABLE_JS": True,
    }
    items = []

    def __init__(self, *args, **kwargs):
        super(NiftyDetailsSpider, self).__init__(*args, **kwargs)
        self.listings = select_listings_missing_details(self.source)[
            :2500
        ]  # TODO REMOVE
        # self.listings = [
        #     {
        #         "bukken_id": "0019138311",
        #         "url": "https://myhome.nifty.com/chuko/ikkodate/osaka/daitoshi/yahoof_0019138311/",
        #     },
        # ]

    def start_requests(self):
        if len(self.listings) > 0:
            listing = self.listings.pop(0)
            yield undetected_request(
                listing["url"], wait_until=WAIT_UNTIL, data=listing
            )

    def parse_item(self, bukken_id, source, driver):
        # Handle scenario where a listing has already been removed.
        presence = parse_bukken_presence(driver)
        if presence:
            description = parse_description(driver)
            upper_table_data = parse_upper_table_data(driver)
            price_yen = upper_table_data["price_yen"]
            address = upper_table_data["address"]
            construction_year = upper_table_data["construction_year"]
            lower_table_data = parse_lower_table_data(driver)
            remarks = lower_table_data["remarks"]

            # Fetch coordinates from driver
            # If coordinates are not found, fetch from db
            # If coordinates are not found, fetch from Google Maps API
            coordinates = parse_coordinates(driver)
            if coordinates["lat"] is None or coordinates["lon"] is None:
                coordinates = select_coordinates(address)
                if coordinates["lat"] is None or coordinates["lon"] is None:
                    self.logger.info(
                        "AKIYA-MART-TASKS GOOGLE MAPS API. bukken_id: {bukken_id} address: {address}".format(
                            bukken_id=bukken_id, address=address
                        )
                    )
                    # DANGER COSTS MONEY
                    coordinates = gelocate(address)

            image_urls = parse_image_urls(driver)

            item = {
                "bukken_id": bukken_id,
                "source": source,
                "lat": coordinates["lat"],
                "lon": coordinates["lon"],
                "is_geocoded": coordinates["is_geocoded"],
                "price_yen": price_yen,
                "address": address,
                "image_urls": image_urls,
                "construction_year": construction_year,
                "description": description,
                "remarks": remarks,
                "needs_update": False,
            }
            return item
        else:
            return None

    def parse(self, response):
        bukken_id = response.request.data["bukken_id"]
        driver = response.request.meta["driver"]

        try:
            item = self.parse_item(bukken_id, self.source, driver)
            if item:
                cond = (
                    item["price_yen"] is not None
                    and item["lat"] is not None
                    and item["lon"] is not None
                )
                if cond:
                    self.items.append(item)
                self.items.append(item)
        except:
            self.logger.exception(
                "AKIYA-MART-TASK PARSING ERROR {}".format(response.request.url)
            )

            # Write to db in chunks
            # This way even if we crash we get some data of for this run
            if len(self.items) >= CHUNK_SIZE:
                self.logger.info(
                    "AKIYA-MART-TASKS: INSERTING {n} ITEMS INTO LISTINGS-DETAILS.".format(
                        n=len(self.items)
                    )
                )
                insert_listings_details(dedupe(self.items))
                self.items = []

        if len(self.listings) > 0:
            next_listing = self.listings.pop(0)
            if next_listing is not None:
                yield undetected_request(
                    next_listing["url"], wait_until=WAIT_UNTIL, data=next_listing
                )

    def close(self, reason):
        if len(self.items) > 0:
            self.logger.info(
                "AKIYA-MART-TASKS: INSERTING {n} ITEMS INTO LISTINGS-DETAILS.".format(
                    n=len(self.items)
                )
            )
            insert_listings_details(dedupe(self.items))
            self.items = []
