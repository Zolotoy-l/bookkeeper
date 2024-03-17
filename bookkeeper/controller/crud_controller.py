from bookkeeper.models.entities import db
import bookkeeper.controller.query_helper as qh
from bookkeeper.view.main_window import MainWindow


class CrudController:
    def __init__(self):
        try:
            db.bind(provider='sqlite', filename='../database.sqlite', create_db=True)  # TODO: Move DB file name to config / dotenv
            db.generate_mapping(create_tables=True)

        except Exception as e:
            print(e)

    def create(self, entity, params):
        if entity == 'Budget':
            qh.add_budget(daily=params['daily'], weekly=params['weekly'],
                          monthly=params['monthly'])
            return

        if entity == 'Expense':
            qh.add_expense(amount=params['amount'], category=params['category'])
            return

        raise NotImplementedError(f'Добавление для сущности {entity} не реализовано!')

    def read(self, entity, id):
        if entity == 'Budget':
            return qh.get_budget()
        if entity == 'Expense':
            return qh.get_expense(id)

        raise NotImplementedError(f'Чтение для сущности {entity} не реализовано!')

    def update(self, entity, params):
        if entity == 'Budget':
            qh.add_budget(daily=params['daily'], weekly=params['weekly'],
                          monthly=params['monthly'])
            return

        raise NotImplementedError(f'Изменение для сущности {entity} не реализовано!')

    def delete(self, entity):
        raise NotImplementedError(f'Удаление для сущности {entity} не реализовано!')

    def get_count(self, entity):
        if entity == 'Expense':
            return qh.get_expense_count()

        raise NotImplementedError(f'Количество объектов для сущности {entity} не реализовано!')