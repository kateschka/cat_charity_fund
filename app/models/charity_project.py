from app.models.base import BaseModel
from sqlalchemy import Column, String


class CharityProject(BaseModel):
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __repr__(self):
        return f'{self.name} ({self.id})'
