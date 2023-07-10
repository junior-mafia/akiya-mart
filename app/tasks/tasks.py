from datetime import datetime
import logging
from app.tasks.repo import insert_rundate
from app import celery, Session
from app.tasks.log_task import log_task
import traceback
import subprocess
from app.tasks.translate import translation_task
from app.tasks.geojson import geojson_task
from celery import chain


logger = logging.getLogger(__name__)
logger_urllib3 = logging.getLogger("urllib3")
logger_urllib3.setLevel(logging.WARNING)


@celery.task
@log_task
def task_rundate():
    try:
        session = Session()
        today = datetime.now().strftime("%Y-%m-%d")
        insert_rundate(session, today)
        return {"run_date": today}
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task rundate: {str(e)}\n{stack_trace}"
        logger.error(error)
    finally:
        session.close()


@celery.task
@log_task
def task_listings_athome(results):
    try:
        run_date = results["run_date"]
        cmd = "scrapy crawl athome -a run_date={run_date}".format(run_date=run_date)
        subprocess.check_output(cmd, shell=True)
        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task listings-athome: {str(e)}\n{stack_trace}"
        logger.error(error)


@celery.task
@log_task
def task_listings_nifty(results):
    try:
        run_date = results["run_date"]
        cmd = "scrapy crawl nifty -a run_date={run_date}".format(run_date=run_date)
        subprocess.check_output(cmd, shell=True)
        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task listings-nifty: {str(e)}\n{stack_trace}"
        logger.error(error)


@celery.task
@log_task
def task_listings_details_athome(results):
    try:
        cmd = "scrapy crawl athome_details"
        subprocess.check_output(cmd, shell=True)
        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = (
            f"Exception during task listings-details-athome: {str(e)}\n{stack_trace}"
        )
        logger.error(error)


@celery.task
@log_task
def task_listings_details_nifty(results):
    try:
        cmd = "scrapy crawl nifty_details"
        subprocess.check_output(cmd, shell=True)
        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = f"Exception during task listings-details-nifty: {str(e)}\n{stack_trace}"
        logger.error(error)


@celery.task
@log_task
def task_listings_details_translate(results):
    try:
        session = Session()
        translation_task(session)
        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = (
            f"Exception during task listings-details-translate: {str(e)}\n{stack_trace}"
        )
        logger.error(error)
    finally:
        session.close()


@celery.task
@log_task
def task_generate_geojson_task(results):
    try:
        session = Session()
        geojson_task(session)
        return results
    except Exception as e:
        stack_trace = traceback.format_exc()
        error = (
            f"Exception during task listings-details-geojson: {str(e)}\n{stack_trace}"
        )
        logger.error(error)
    finally:
        session.close()


def generate_task_run_all():
    insert_rundate = chain(task_rundate.s())
    scrape_listings = chain(
        task_listings_athome.s(),
        task_listings_nifty.s(),
    )
    scrape_listings_details = chain(
        task_listings_details_athome.s(),
        task_listings_details_nifty.s(),
    )
    translate = chain(task_listings_details_translate.s())
    generate_geojson = chain(task_generate_geojson_task.s())
    chained_task = chain(
        insert_rundate,
        scrape_listings,
        scrape_listings_details,
        translate,
        generate_geojson,
    )
    return chained_task
