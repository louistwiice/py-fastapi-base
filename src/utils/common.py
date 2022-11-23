import string
import rstr


def generate_string(size: int = 12):
    return rstr.rstr(string.ascii_letters, size)


def generate_token(size: int = 5):
    return rstr.rstr(string.digits, size)
