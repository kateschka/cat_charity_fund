from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from app.core.error_message import ErrorMessage
from app.models import CharityProject


def check_if_project_exists(charity_project: Optional[CharityProject]):
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessage.PROJECT_NOT_FOUND
        )


def check_if_project_with_same_name_exists(
    charity_project_name: str,
    charity_project: CharityProject
):
    if charity_project and charity_project_name == charity_project.name:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.NOT_UNIQUE_PROJECT_NAME
        )


def check_if_full_amount_is_less_than_invested_amount(
    new_full_amount: int,
    invested_amount: int,
):
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.INVESTED_AMOUNT_GREATER_THAN_FULL_AMOUNT
        )


def check_if_project_is_closed(
    charity_project: CharityProject
):
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CLOSED_PROJECT_EDIT
        )


def check_if_project_was_invested(
    charity_project: CharityProject
):
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.INVESTED_PROJECT_DELETE
        )