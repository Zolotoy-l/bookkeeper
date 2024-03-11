from datetime import date
from pony.orm import *


db = Database()


class Budget(db.Entity):
    id = PrimaryKey(int, auto=True)
    monthly = Required(float)
    weekly = Required(float)
    daily = Required(float)


class Expense(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Required(int)
    expense_date = Required(date)
    added_date = Required(date)
    comment = Optional(str)
    category = Required('Category')


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    expenses = Set(Expense)
    parent = Optional('Category', reverse='parent')



db.generate_mapping()