from pony.orm import *
from bookkeeper.models.entities import Budget, Expense
from datetime import date


@db_session
def add_budget(monthly, weekly, daily):
    try:
        Budget(daily=daily, weekly=weekly, monthly=monthly)
    except Exception as e:
        print(e)  # TODO: This should be sent to GUI in a user-friendly manner


@db_session
def get_budget():
    try:
        q = Budget.select().order_by(desc(Budget.id)).limit(1).to_list()
        if len(q):
            budget = q[0]
            return tuple([budget.daily, budget.weekly, budget.monthly])  # TODO: return the object itself for GUI?
        else:
            return tuple([0,0,0])
    except Exception as e:
        print(e)  # TODO: This should be sent to GUI in a user-friendly manner


@db_session
def add_expense(amount, category):
    try:
        Expense(expense_date=date.today(), amount=amount, category=category, comment='')
    except Exception as e:
        print(e)


@db_session
def get_expense(id):
    try:
        expn = Expense.get(id=id)
        return tuple([expn.expense_date, expn.amount, expn.category, expn.comment])
    except Exception as e:
        print(e)


@db_session
def get_expense_count():
    try:
        e = Expense.select().order_by(desc(Expense.id))[:1]
        if len(e):
            str_num = int(e[0].id)
            return str_num
        else:
            return 0
    except Exception as e:
        print(e)


@db_session
def update_expense(expense_date, amount, category, comment, row):
    try:
        Expense[row].expense_date = expense_date
        Expense[row].amount = amount
        Expense[row].category = category
        Expense[row].comment = comment
        commit()
    except Exception as e:
        print(e)
