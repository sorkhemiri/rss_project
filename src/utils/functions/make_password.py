import hashlib

from settings import env_config


def make_password(password: str):
    salt = env_config.SECRET_KEY
    password_hash = hashlib.sha256((salt + password).encode()).hexdigest()
    return password_hash
