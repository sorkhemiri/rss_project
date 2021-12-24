import secrets


def make_random_hex(n_bytes: int = 12):
    return secrets.token_hex(n_bytes)
