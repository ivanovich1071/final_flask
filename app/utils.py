from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    """Хэширование пароля."""
    return generate_password_hash(password)

def check_password(hashed_password, password):
    """Проверка пароля."""
    return check_password_hash(hashed_password, password)