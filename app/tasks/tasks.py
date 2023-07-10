from datetime import datetime
import logging
from app.tasks.repo import insert_rundate
from app import celery, Session
from app.tasks.log_task import log_task
import traceback
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from app.tasks.spiders.athome import AtHomeSpider
from app.tasks.spiders.nifty import NiftySpider
from twisted.internet import defer
import crochet
from crochet import setup, run_in_reactor
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor



crochet.setup()


logger = logging.getLogger(__name__)
logger_urllib3 = logging.getLogger('urllib3')
logger_urllib3.setLevel(logging.WARNING)


@celery.task
@log_task
def task_rundate():
    try:
        session = Session()
        today = datetime.now().strftime("%Y-%m-%d")
        insert_rundate(today, session)
        return {"run_date": today}
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task rundate: {str(e)}\n{stack_trace}"
        logger.error(error)
    finally:
        session.close()


@celery.task
@log_task
@crochet.wait_for(timeout=12*60*60)  # timeout after 12 hours
def task_listings_athome(results):
    try:
        session = Session()
        run_date = results["run_date"]
        process = CrawlerProcess(get_project_settings())

        d = defer.Deferred()
        d.addCallback(lambda _: process.crawl(AtHomeSpider, session=session, run_date=run_date))
        d.addBoth(lambda _: process.stop())
        d.callback(None)

        return d
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task listings-athome: {str(e)}\n{stack_trace}"
        logger.error(error)
    finally:
        session.close()


@celery.task
@log_task
def task_listings_nifty(results):
    try:
        session = Session()
        run_date = results["run_date"]

        runner = CrawlerRunner(get_project_settings())

        @run_in_reactor
        def crawl():
            print("Starting crawl...")
            d = runner.crawl(NiftySpider, session=session, run_date=run_date)
            d.addBoth(lambda _: print("Crawl finished."))
            return d

        print("Before calling crawl.")
        crawl()
        print("After calling crawl.")

        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task listings-nifty: {str(e)}\n{stack_trace}"
        logger.error(error)
    finally:
        session.close()


