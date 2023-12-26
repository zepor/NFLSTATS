from functools import wraps
from src.utils.log import be_logger

def log_and_catch_exceptions(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            be_logger.error(f"Exception in {func.__name__}: {e}")
            raise
    return func_wrapper
