import scrapy
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from app.tasks.undetected_request import undetected_request
from app.tasks.repo import insert_listings
import os

ENVIRONMENT = os.environ["ENVIRONMENT"]

# WAIT_UNTIL = EC.presence_of_element_located((By.CSS_SELECTOR, "div#resultSubContents"))
WAIT_UNTIL = EC.presence_of_element_located((By.CSS_SELECTOR, "div.buy_list"))

# RESULTS_PER_PAGE does not actually seem to have any effect when we &pnum=RESULTS_PER_PAGE in the URL
# What is even stranger is when we visit the URL in the browser it will return a hardcoded 40 bukkens.
# But when we run headless chrome with javascript disabled its 20 bukkens returned! Thats why we hardcode
# to 20 here as a reminder that this is what is happening.
RESULTS_PER_PAGE = 20
BASE_URL = "https://myhome.nifty.com/chuko/ikkodate/search/?subtype=buh&sort1=money1-asc&b2=30000000&page={page_num}"
CHUNK_SIZE = 2000


def parse_url(bukken):
    url = bukken.find_element(
        By.CSS_SELECTOR, "div.nayose_head > h2.link > p a"
    ).get_attribute("href")
    return url


def url_is_known_bad(url):
    if "https://myhome.nifty.com/ikkodate/detail/?url" in url:
        return True
    else:
        return False


def parse_bukken_id_from_url(url):
    # Filter out URLs that don't match the pattern
    # GOOD "https://myhome.nifty.com/chuko/ikkodate/niigata/joetsushi/suumof_70811574/"
    # GOOD https://myhome.nifty.com/chuko/ikkodate/hyogo/itamishi/tryellf_mss000012_453600R/
    # GOOD https://myhome.nifty.com/chuko/ikkodate/kagawa/mitoyoshi/homesf_01472870000032/
    # GOOD https://myhome.nifty.com/chuko/ikkodate/hokkaido/hiroogunhiroocho/yahoof_0019447847/
    # BAD "https://myhome.nifty.com/ikkodate/detail/?url=https%3A%2F%2Fwww.pitat.com%2FbuyDetail%2FAAX0376.html%3Fcvid%3Dnf&=&pref=&b2=27593000&psid=5d06be7005cfe94c86397c84a47ad40f8f7ad327d0509c4766afb420c87978da"
    pattern = r"^https://myhome\.nifty\.com/chuko/ikkodate/.+?/[^_]*_(\w+)/?$"
    match = re.search(pattern, url)
    if match:
        return match.group(1)


def dedupe(items):
    seen = set()
    return [
        x
        for x in items
        if not (x["bukken_id"], x["source"]) in seen
        and not seen.add((x["bukken_id"], x["source"]))
    ]


def find_duplicates(items):
    seen = set()
    duplicates = []
    for x in items:
        if (x["bukken_id"], x["source"]) in seen:
            duplicates.append(x)
        else:
            seen.add((x["bukken_id"], x["source"]))
    return duplicates


class NiftySpider(scrapy.Spider):
    name = "nifty"
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "app.tasks.undetected_middleware.UndetectedMiddleware": 543,
        },
        "LOG_LEVEL": "INFO",
        "DISABLE_JS": True,
        # 'CONCURRENT_REQUESTS': 1,
    }

    def __init__(self, session, run_date=None, *args, **kwargs):
        super(NiftySpider, self).__init__(*args, **kwargs)
        self.session = session
        self.run_date = run_date
        self.items = []

    def start_requests(self):
        # We are able to find a URL on the nifty site that will return ALL bukken
        # So we are able to start from the last page we scraped and work forwards
        # if this task is interrupted and restarted.
        # current_count = get_current_count("nifty")
        starting_page_num = 1  # + (current_count // RESULTS_PER_PAGE)
        self.logger.info(
            "AKIYA-MART-TASKS: STARTING FROM PAGE: {page_num}".format(
                page_num=starting_page_num
            )
        )
        url = BASE_URL.format(
            page_num=starting_page_num,
        )
        yield undetected_request(url=url, wait_until=WAIT_UNTIL)

    def parse(self, response):
        driver = response.request.meta["driver"]
        bukkens = driver.find_elements(By.CSS_SELECTOR, "div.nayose") or []

        for bukken in bukkens:
            url = parse_url(bukken)
            if not url:
                self.logger.warning("AKIYA-MART-TASKS: COULD NOT PARSE URL FROM BUKKEN")
                continue

            bukken_id = parse_bukken_id_from_url(url)
            if not bukken_id:
                if url_is_known_bad(url):
                    continue
                else:
                    self.logger.warning(
                        "AKIYA-MART-TASKS: COULD NOT PARSE BUKKEN_ID FROM URL: {url}".format(
                            url=url
                        )
                    )
                    continue

            item = {
                "bukken_id": bukken_id,
                "source": "nifty",
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

        elements = driver.find_elements(By.CSS_SELECTOR, "div.resultNumArea li.mg3")
        next_page_url = None
        for element in elements:
            if "次へ" in element.text:
                next_page_url = element.find_element(By.TAG_NAME, "a").get_attribute(
                    "href"
                )
                break

        if next_page_url is not None:
            yield undetected_request(next_page_url, wait_until=WAIT_UNTIL)
        else:
            self.logger.info(
                "AKIYA-MART-TASKS NIFTY: ENDING ON PAGE {url}.".format(
                    url=response.request.url
                )
            )

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
