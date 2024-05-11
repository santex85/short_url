from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Конфигурация базы данных
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Определение модели базы данных для ссылок
class Link(Base):
    __tablename__ = 'links'  # имя таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)  # уникальный идентификатор для каждой записи
    original_url = Column(String, unique=True, nullable=False)  # оригинальная длинная ссылка
    short_url = Column(String, index=True)  # сгенерированная короткая ссылка


# Создание таблиц, если они еще не созданы
Base.metadata.create_all(bind=engine)
