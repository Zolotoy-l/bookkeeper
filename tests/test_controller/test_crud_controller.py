import datetime

import pytest
from bookkeeper.controller.crud_controller import CrudController


@pytest.fixture
def crudctrl():
    return CrudController()


def test_add_and_read_budget(crudctrl):
    crudctrl.create('Budget', {'monthly': 100_000,
                               'weekly': 25_000,
                               'daily': 4_000})
    budget_tup = crudctrl.read('Budget', None)
    assert budget_tup == (4000.0, 25000.0, 100000.0)


def test_add_and_read_category(crudctrl):
    crudctrl.create('Category', {'name': 'biba'})
    category_tup = crudctrl.read('Category', None)
    assert category_tup == ('biba',)


def test_add_and_read_expense(crudctrl):
    crudctrl.create('Expense', {'amount': 250,
                                'category': 'biba'})
    num_row = crudctrl.get_count('Expense')
    expense_tup = crudctrl.read('Expense', num_row-1)
    assert expense_tup == (datetime.date.today(), 250, 'biba', '')


def test_update_expense(crudctrl):
    crudctrl.create('Category', {'name': 'boba'})
    num_row = crudctrl.get_count('Expense')
    crudctrl.update('Expense', {'date': datetime.date.today(),
                                'amount': 150,
                                'category': 'boba',
                                'comment': 'test comment',
                                'row': num_row-1})
    expense_tup = crudctrl.read('Expense', num_row-1)
    assert expense_tup == (datetime.date.today(), 150, 'boba', 'test comment')


def test_update_category(crudctrl):
    crudctrl.update('Category', {'prev_name': 'boba',
                                 'new_name': 'abob'})
    num_row = crudctrl.get_count('Expense')
    expense_tup = crudctrl.read('Expense', num_row - 1)
    assert expense_tup == (datetime.date.today(), 150, 'abob', 'test comment')
    category_tup = crudctrl.read('Category', None)
    assert category_tup == ('biba', 'abob')


def test_delete_expense(crudctrl):
    num_row = crudctrl.get_count('Expense')
    crudctrl.delete('Expense', {'row': num_row-1})

    expense_tup = crudctrl.read('Expense', num_row-1)
    assert expense_tup == None

def test_delete_category(crudctrl):
    crudctrl.delete('Category', {'name': 'biba'})
    category_tup = crudctrl.read('Category', None)
    assert category_tup == ('abob',)