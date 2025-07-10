from enum import Enum


class ErrorMessage(str, Enum):
    CLOSED_PROJECT_EDIT = 'Закрытый проект нельзя редактировать!'
    INVESTED_AMOUNT_GREATER_THAN_FULL_AMOUNT = (
        'Сумма инвестиций не может быть больше полной суммы проекта!'
    )
    INVALID_FULL_AMOUNT = 'Сумма инвестиций не может быть меньше или равна 0!'
    INVESTED_PROJECT_DELETE = (
        'В проект были внесены средства, его нельзя удалить!'
    )
    REQUEST_EMPTY_BODY = 'Запрос не может быть пустым!'
    NOT_UNIQUE_PROJECT_NAME = 'Проект с таким именем уже существует!'
    PROJECT_NOT_FOUND = 'Проект не найден!'
