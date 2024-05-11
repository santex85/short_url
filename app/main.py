from typing import Dict

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import Link
from app.pydantic_models import LinkCreate
from app.utils import get_db, generate_short_link

app = FastAPI()


# API-эндпоинт для создания новой ссылки
@app.post("/")
def create_link(link: LinkCreate, db: Session = Depends(get_db)):
    try:
        # Проверка валидности URL
        valid_url = LinkCreate.validate_url(link.original_url)

        # Начало транзакции
        db.begin()

        # Поиск существующей ссылки
        db_link = db.query(Link).filter(Link.original_url == valid_url).first()
        if db_link:
            return db_link

        # Генерация короткой ссылки и создание новой записи
        short_url = generate_short_link()
        db_link = Link(original_url=valid_url, short_url=short_url)
        db.add(db_link)

        # Фиксация транзакции
        db.commit()

        # Возвращаем новую ссылку
        db.refresh(db_link)
        return db_link

    except Exception as e:
        # Откатываем транзакцию при ошибке
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        # Закрытие сессии
        db.close()


# API-эндпоинт для получения оригинальной ссылки по короткой
def read_link(short_url: str, db: Session = Depends(get_db)) -> Dict[str, str]:
    db_link = db.query(Link).filter(Link.short_url == short_url).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")  # если не найдено, возвращаем ошибку
    return {"original_url": db_link.original_url}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
