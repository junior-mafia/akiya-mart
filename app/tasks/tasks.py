from datetime import datetime
import logging
from app.tasks.repo import insert_rundate
from app import celery, Session
from app.tasks.log_task import log_task
import traceback
import subprocess


logger = logging.getLogger(__name__)
logger_urllib3 = logging.getLogger('urllib3')
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
        cmd = "scrapy crawl athome -a run_date={run_date}".format(
            run_date=run_date
        )
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
        cmd = "scrapy crawl nifty -a run_date={run_date}".format(
            run_date=run_date
        )
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
        error = f"Exception during task listings-details-athome: {str(e)}\n{stack_trace}"
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

