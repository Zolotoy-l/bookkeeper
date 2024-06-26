"""File with entities for db"""
from datetime import date
from pony.orm import *


db = Database()


class Category(db.Entity):
    """Category entity"""
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    expenses = Set('Expense')


class Expense(db.Entity):
    """Expense entity for storing its info"""
    id = PrimaryKey(int, auto=True)
    expense_date = Required(date, default=date.today())
    amount = Required(float)
    category = Required(Category)
    comment = Optional(str)


class Budget(db.Entity):
    """Entity for storing budget"""
    id = PrimaryKey(int, auto=True)
    daily = Required(float, default=2000)
    weekly = Required(float, default=14000)
    monthly = Required(float, default=56000)
