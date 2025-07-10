from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud import donation_crud, charity_project_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, UserDonation
from app.services.investments import invest

router = APIRouter(prefix='/donation', tags=['donation'])


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_all_donations(session)


@router.post(
    '/',
    response_model=UserDonation,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    charity_projects_to_update = invest(
        [new_donation],
        await charity_project_crud.get_all_unclosed_charity_projects(session)
    )

    session.add_all(charity_projects_to_update)
    await session.commit()
    await session.refresh(new_donation)

    return new_donation


@router.get(
    '/my',
    response_model=list[UserDonation],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await donation_crud.get_by_user(user, session)