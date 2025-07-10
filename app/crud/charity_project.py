from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_id(
            self,
            charity_project_id: int,
            session: AsyncSession,
    ):
        return await self.get(charity_project_id, session)

    async def get_current_active_project(
            self,
            session: AsyncSession,
    ):
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_all_unclosed_charity_projects(
            self,
            session: AsyncSession,
    ):
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        return result.scalars().all()

    async def get_all_charity_projects(
            self,
            session: AsyncSession,
    ):
        result = await session.execute(select(CharityProject))
        return result.scalars().all()

    async def update_project(
            self,
            charity_project: CharityProject,
            update_data: CharityProjectUpdate,
            session: AsyncSession,
    ):
        project = await self.update(charity_project, update_data, session)

        if project.full_amount == project.invested_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
            session.add(project)
            await session.commit()
            await session.refresh(project)

        return project


charity_project_crud = CRUDCharityProject(CharityProject)
