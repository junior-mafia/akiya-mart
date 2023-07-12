import os
from scrapy import signals
from scrapy.http import HtmlResponse
import undetected_chromedriver as uc
from app.tasks.undetected_request import UndetectedRequest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import logging


class UndetectedMiddleware:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)

    @classmethod
    def from_crawler(cls, crawler):
        options = uc.ChromeOptions()
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--blink-settings=imagesEnabled=false")
        prefs = {}
        prefs["profile.managed_default_content_settings.images"] = 2

        if crawler.spider.custom_settings.get("DISABLE_JS"):
            # https://stackoverflow.com/questions/73959812/selenium-python-how-can-i-disable-javascript-while-using-headless-chrome
            prefs["webkit.webprefs.javascript_enabled"] = False
            prefs["profile.content_settings.exceptions.javascript.*.setting"] = 2
            prefs["profile.default_content_setting_values.javascript"] = 2
            prefs["profile.managed_default_content_settings.javascript"] = 2
            options.add_argument("--disable-javascript")
            options.add_argument("--headless=new")  # Required for Heroku
        else:
            options.add_argument("--headless")  # Required for Heroku
            pass
        options.add_experimental_option("prefs", prefs)

        uc.TARGET_VERSION = 114
        driver = uc.Chrome(
            executable_path=os.environ.get(
                "CHROMEDRIVER_PATH", "/opt/homebrew/bin/chromedriver"
            ),
            options=options,
        )

        middleware = cls(driver=driver)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if not isinstance(request, UndetectedRequest):
            return None

        max_retries = 5
        retries = 0
        while retries < max_retries:
            try:
                self.driver.get(request.url)

                if request.wait_until:
                    self.wait.until(request.wait_until)
                else:
                    logging.warning("WARNING SLEEPING IS INEFFICIENT")
                    time.sleep(5)

                request.meta.update({"driver": self.driver})
                return HtmlResponse(
                    self.driver.current_url,
                    body="<!DOCTYPE html><html><head></head><body></body></html>",  # Dummy body
                    encoding="utf-8",
                    request=request,
                )
            except TimeoutException:
                logging.error(
                    f"TimeoutException occurred. Retrying {retries+1}/{max_retries}..."
                )
                retries += 1
                time.sleep(300)  # Wait for 5 minutes before retrying

        # If the request still fails after max_retries, raise the exception
        raise TimeoutException(
            f"Unable to process request after {max_retries} attempts"
        )

    def spider_closed(self):
        self.driver.quit()


# options.add_argument("--disable-gpu")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--disable-background-networking")
# options.add_argument("--disable-background-timer-throttling")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-infobars")
# options.add_argument("--disable-setuid-sandbox")
# options.add_argument("--disable-accelerated-2d-canvas")
# options.add_argument("--no-first-run")
# options.add_argument("--no-zygote")
# options.add_argument("--single-process")
# options.add_argument("--disable-remote-fonts")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
# options.add_argument("--disable-webgl")
# options.add_argument("--disable-software-rasterizer")
# options.add_argument("--start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
