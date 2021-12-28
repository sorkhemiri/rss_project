import functools
import time


def retry(times, wait):
    def retry_it(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            how_many = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                except Exception as ex:
                    if how_many > times:
                        raise ex
                    else:
                        how_many += 1
                        time.sleep(wait)
                else:
                    return result

        return wrapper

    return retry_it
