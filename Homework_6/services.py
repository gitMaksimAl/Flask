import bcrypt


def get_hash(passwd: str) -> str:
    return bcrypt.hashpw(passwd.encode("utf-8"),
                         bcrypt.gensalt()).decode("utf-8")
