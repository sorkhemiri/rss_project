import datetime


def calculate_expiration_interval(interval: int = 0):
    return (datetime.datetime.utcnow() + datetime.timedelta(seconds=interval)).isoformat(timespec='seconds')