# Функция для генерации короткой ссылки
import random
import string

from app.db import SessionLocal


def generate_short_link():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))  # генерация случайной строки длиной 6 символов
    return short_url


# Вспомогательная функция для создания сессии с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()