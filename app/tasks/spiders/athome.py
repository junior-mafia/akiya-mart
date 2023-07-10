from scrapy import Spider
from app.tasks.undetected_request import undetected_request
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.tasks.repo import insert_listings
import os

ENVIRONMENT = os.environ["ENVIRONMENT"]

PREFECTURES = [
    "aichi",
    "akita",
    "aomori",
    "chiba",
    "ehime",
    "fukui",
    "fukuoka",
    "fukushima",
    "gifu",
    "gunma",
    "hiroshima",
    "hokkaido",
    "hyogo",
    "ibaraki",
    "ishikawa",
    "iwate",
    "kagawa",
    "kagoshima",
    "kanagawa",
    "kochi",
    "kumamoto",
    "kyoto",
    "mie",
    "miyagi",
    "miyazaki",
    "nagano",
    "nagasaki",
    "nara",
    "niigata",
    "oita",
    "okayama",
    "okinawa",
    "osaka",
    "saga",
    "saitama",
    "shiga",
    "shimane",
    "shizuoka",
    "tochigi",
    "tokushima",
    "tokyo",
    "tottori",
    "toyama",
    "wakayama",
    "yamagata",
    "yamaguchi",
    "yamanashi",
]


WAIT_UNTIL = EC.presence_of_element_located((By.CSS_SELECTOR, "div#mainBody"))

RESULTS_PER_PAGE = 50
BASE_URL = "https://www.athome.co.jp/kodate/chuko/{prefecture}/list/page{page_num}/?RND_TIME_PRM=61853&RND_MODE=&ITEMNUM={results_per_page}&PRICETO=kp106"
CHUNK_SIZE = 2000


def parse_url(bukken):
    url = bukken.find_element(By.CSS_SELECTOR, "a.kslisttitle").get_attribute("href")
    return url


def parse_bukken_id(bukken):
    bukken_id = bukken.get_attribute("data-bukken-no")
    return bukken_id


def parse_next_page_url(driver):
    paging_elements = driver.find_elements(By.CSS_SELECTOR, "ul.paging li")
    next_page_url = None
    for paging_element in paging_elements:
        if "次へ" in paging_element.text:
            next_page_url = (
                paging_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                + "&PRICETO=kp106"
            )
            break
    return next_page_url


def dedupe(items):
    seen = set()
    return [
        x
        for x in items
        if not (x["bukken_id"], x["source"]) in seen
        and not seen.add((x["bukken_id"], x["source"]))
    ]


class AtHomeSpider(Spider):
    name = "athome"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "app.tasks.undetected_middleware.UndetectedMiddleware": 543,
        },
        "LOG_LEVEL": "INFO",
        "DISABLE_JS": False,
    }
    prefectures = PREFECTURES

    def __init__(self, session, run_date=None, *args, **kwargs):
        super(AtHomeSpider, self).__init__(*args, **kwargs)
        self.session = session
        self.run_date = run_date
        self.items = []

    def start_requests(self):
        # We are not able to find a URL on the athome website that returns a
        # FULL list of bukken. We don't store the prefecture information either so
        # we can't use that either. For now, restart at beginning everytime.
        starting_page_num = 1
        self.logger.info(
            "AKIYA-MART-TASKS: STARTING FROM PAGE: {page_num}".format(
                page_num=starting_page_num
            )
        )
        prefecture = self.prefectures.pop(0)
        url = BASE_URL.format(
            page_num=starting_page_num,
            prefecture=prefecture,
            results_per_page=RESULTS_PER_PAGE,
        )
        yield undetected_request(url=url, wait_until=WAIT_UNTIL)

    def parse(self, response):
        driver = response.request.meta["driver"]
        bukkens = (
            driver.find_elements(
                By.CSS_SELECTOR, "div.object.boxHover.boxHoverLinkStop"
            )
            or []
        )
        for bukken in bukkens:
            url = parse_url(bukken)
            if not url:
                self.logger.warning("AKIYA-MART-TASKS: COULD NOT PARSE URL FROM BUKKEN")
                continue

            bukken_id = parse_bukken_id(bukken)
            if not bukken_id:
                self.logger.warning(
                    "AKIYA-MART-TASKS: COULD NOT PARSE BUKKEN_ID FROM BUKKEN: {url}".format(
                        url=url
                    )
                )
                continue

            item = {
                "bukken_id": bukken_id,
                "source": "athome",
                "url": url,
                "first_seen_at": self.run_date,
                "last_seen_at": self.run_date,
            }
            self.items.append(item)

        # Write to db in chunks
        # This way even if we crash we get some data of for this run
        if len(self.items) >= CHUNK_SIZE:
            deduped_items = dedupe(self.items)
            self.logger.info(
                "AKIYA-MART-TASKS: INSERTING {n} ITEMS INTO LISTINGS.".format(
                    n=len(deduped_items)
                )
            )
            insert_listings(self.session, deduped_items)
            self.items = []
            # Return after one chunk in dev
            if ENVIRONMENT == "DEV":
                return

        next_page_url = parse_next_page_url(driver)
        if next_page_url is not None:
            yield undetected_request(next_page_url, wait_until=WAIT_UNTIL)
        else:
            if len(self.prefectures) > 0:
                prefecture = self.prefectures.pop(0)
                page_num = 1
                url = BASE_URL.format(
                    page_num=page_num,
                    prefecture=prefecture,
                    results_per_page=RESULTS_PER_PAGE,
                )
                yield undetected_request(url=url, wait_until=WAIT_UNTIL)

    def close(self, reason):
        if len(self.items) > 0:
            deduped_items = dedupe(self.items)
            self.logger.info(
                "AKIYA-MART-TASKS: INSERTING {n} ITEMS INTO LISTINGS.".format(
                    n=len(deduped_items)
                )
            )
            insert_listings(self.session, deduped_items)
            self.items = []
