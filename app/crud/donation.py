from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import Donation
from app.models.user import User


class CRUDDonation(CRUDBase):

    async def get_by_user(
            self,
            user: User,
            session: AsyncSession,
    ):
        donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return donations.scalars().all()

    async def get_all_donations(
            self,
            session: AsyncSession,
    ):
        donations = await session.execute(select(Donation))
        return donations.scalars().all()

    async def get_all_uninvested_donations(
            self,
            session: AsyncSession,
    ):
        donations = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date)
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)