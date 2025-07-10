from app.models.base import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String, nullable=True)

    user = relationship('User', back_populates='donations', cascade='delete')

    def __repr__(self):
        return f'Пользователь {self.user_id} помог ' \
               f'котикам на сумму ({self.invested_amount})'
