from passlib.hash import pbkdf2_sha256


def hashed_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)


def verify_password(clear_password: str, hashed_pass: str) -> bool:
    return pbkdf2_sha256.verify(clear_password, hashed_pass)

