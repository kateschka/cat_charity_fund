from datetime import datetime
from app.models import Donation, CharityProject
from app.models.base import BaseModel


def close_entity(entity: BaseModel):
    entity.fully_invested = True
    entity.close_date = datetime.now()


def invest(
    donations: list[Donation],
    charity_projects: list[CharityProject]
) -> list[BaseModel]:

    modified = set()

    for project in charity_projects:
        if project.fully_invested:
            continue

        if project.invested_amount == project.full_amount:
            project.fully_invested = True
            project.close_date = datetime.now()
            modified.append(project)
            continue

        for donation in donations:
            if donation.fully_invested:
                continue

            amount_to_invest = min(
                project.full_amount - project.invested_amount,
                donation.full_amount - donation.invested_amount
            )
            project.invested_amount += amount_to_invest
            donation.invested_amount += amount_to_invest
            modified.add(donation)

            if project.invested_amount == project.full_amount:
                close_entity(project)

            if donation.invested_amount == donation.full_amount:
                close_entity(donation)

        modified.add(project)

    return modified
