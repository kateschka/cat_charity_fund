from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_if_project_with_same_name_exists,
    check_if_project_is_closed,
    check_if_full_amount_is_less_than_invested_amount,
    check_if_project_was_invested,
    check_if_project_exists,
)
from app.core.user import current_superuser
from app.crud import charity_project_crud, donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.core.db import get_async_session
from app.models.user import User
from app.services.investments import invest


router = APIRouter(prefix='/charity_project', tags=['charity_project'])


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    project_from_db = await charity_project_crud.get_by_attribute(
        'name', charity_project.name, session
    )

    check_if_project_with_same_name_exists(
        charity_project.name, project_from_db
    )

    new_project = await charity_project_crud.create(
        charity_project, session
    )

    modified_objects = invest(
        await donation_crud.get_all_uninvested_donations(session),
        [new_project]
    )

    session.add_all(modified_objects)
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_all_charity_projects(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    charity_project: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project_from_db_by_id = (
        await charity_project_crud.get_by_attribute(
            'id', project_id, session
        )
    )

    check_if_project_exists(charity_project_from_db_by_id)

    charity_project_from_db_by_name = (
        await charity_project_crud.get_by_attribute(
            'name', charity_project.name, session
        )
    )

    check_if_project_with_same_name_exists(
        charity_project.name, charity_project_from_db_by_name
    )
    check_if_project_is_closed(charity_project_from_db_by_id)

    if charity_project.full_amount is not None:
        check_if_full_amount_is_less_than_invested_amount(
            charity_project.full_amount,
            charity_project_from_db_by_id.invested_amount
        )

    charity_project_from_db_by_id = await charity_project_crud.update_project(
        charity_project_from_db_by_id, charity_project, session
    )

    return charity_project_from_db_by_id


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project_from_db = await charity_project_crud.get_by_attribute(
        'id', project_id, session
    )
    check_if_project_exists(charity_project_from_db)
    check_if_project_was_invested(charity_project_from_db)
    return await charity_project_crud.remove(
        charity_project_from_db, session
    )