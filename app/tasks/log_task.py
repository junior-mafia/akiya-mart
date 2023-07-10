import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger(__name__)

def log_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        logger.info(f"AKIYA-MART-TASKS: STARTING TASK: TIME: {datetime.now()}: NAME: {task_name}")
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error occurred during task {task_name}: {e}")
        finally:
            logger.info(f"AKIYA-MART-TASKS: ENDING TASK: TIME: {datetime.now()}: NAME: {task_name}")
        return result
    return wrapper
