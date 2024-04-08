"""CRUD controller file"""
from bookkeeper.models.entities import db
import bookkeeper.controller.query_helper as qh


class CrudController:
    """CRUD controller over db"""
    def __init__(self):
        try:
            db.bind(provider='sqlite', filename='../database.sqlite', create_db=True)
            db.generate_mapping(create_tables=True)

        except Exception as e:
            print(e)

    def create(self, entity, params):
        """create entity in db"""
        if entity == 'Budget':
            qh.add_budget(daily=params['daily'], weekly=params['weekly'],
                          monthly=params['monthly'])
            return

        if entity == 'Expense':
            qh.add_expense(amount=params['amount'], category=params['category'])
            return

        if entity == 'Category':
            qh.add_category(name=params['name'])
            return

        raise NotImplementedError(f'Добавление для сущности {entity} не реализовано!')

    def read(self, entity, row):
        """return entity data from db"""
        if entity == 'Budget':
            return qh.get_budget()
        if entity == 'Expense':
            return qh.get_expense(row)
        if entity == 'Category':
            return qh.get_category()
        if entity == 'Expense_sum':
            return qh.get_expense_sum()

        raise NotImplementedError(f'Чтение для сущности {entity} не реализовано!')

    def update(self, entity, params):
        """update entity data in db"""
        if entity == 'Budget':
            qh.add_budget(daily=params['daily'], weekly=params['weekly'],
                          monthly=params['monthly'])
            return
        if entity == 'Expense':
            qh.update_expense(expense_date=params['date'], amount=params['amount'],
                              category=params['category'], comment=params['comment'],
                              row=params['row'])
            return
        if entity == 'Category':
            qh.update_category(prev_name=params['prev_name'], new_name=params['new_name'])
            return

        raise NotImplementedError(f'Изменение для сущности {entity} не реализовано!')

    def delete(self, entity, params):
        """delete entity from, db"""
        if entity == 'Expense':
            qh.delete_expense(row=params['row'])
            return
        if entity == 'Category':
            qh.delete_category(name=params['name'])
            return
        raise NotImplementedError(f'Удаление для сущности {entity} не реализовано!')

    def get_count(self, entity):
        """return count of entities in db"""
        if entity == 'Expense':
            return qh.get_expense_count()
        raise NotImplementedError(f'Количество объектов для сущности '
                                  f'{entity} не реализовано!')
