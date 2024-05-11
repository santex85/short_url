# Pydantic модель для получения данных от пользователя
import validators
from pydantic import BaseModel


class LinkCreate(BaseModel):
    original_url: str

    @classmethod
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError('Invalid URL')
        return v
