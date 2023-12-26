from src.utils.log import be_logger
def log_and_catch_exceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            be_logger.error(f"Error in {func.__name__}: {e}")
# sourcery skip: raise-specific-error
            raise Exception(f"Error in {func.__name__}: {e}")
    return func_wrapper