import bcrypt

__all__ = ['get_password_hash']


def __validate_password(password) -> str:
    """Валидатор пароля"""
    if len(password) < 8:
        raise ValueError('Пароль должен содержать как минимум 8 символов')
    if not any(char.isdigit() for char in password):
        raise ValueError('Пароль должен содержать как минимум одну цифру')
    if not any(char.isupper() for char in password):
        raise ValueError('Пароль должен содержать как минимум одну заглавную букву')
    return password


def get_password_hash(password: str) -> str:
    """ Генерирует хеш заданного пароля."""
    __validate_password(password)
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
