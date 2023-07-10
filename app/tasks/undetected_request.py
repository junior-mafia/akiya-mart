from scrapy import Request


def undetected_request(url, **kwargs):
    return UndetectedRequest(
        url=url,
        method="GET",
        meta={"selenium": True},
        **kwargs,
    )


class UndetectedRequest(Request):
    def __init__(self, wait_until=None, data=None, *args, **kwargs):
        self.wait_until = wait_until
        self.data = data
        super().__init__(*args, **kwargs)
