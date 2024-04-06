from pony.orm import *
from bookkeeper.models.entities import Budget, Expense, Category
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
        q = Category.select(lambda c: c.name is category)
        cats = list(q)
        if len(cats) == 1:
            cat = cats[0]
            Expense(expense_date=date.today(), amount=amount, category=cat, comment='')
    except Exception as e:
        print(e)


@db_session
def get_expense(row):
    try:
        expenses = list(Expense.select().order_by(Expense.id))
        expn = expenses[row]
        return tuple([expn.expense_date, expn.amount, expn.category.name, expn.comment])
    except Exception as e:
        print(e)


@db_session
def get_expense_count():
    try:
        e = list(Expense.select().order_by(Expense.id))
        return len(e)
    except Exception as e:
        print(e)


@db_session
def update_expense(expense_date, amount, category, comment, row):
    try:
        q = Category.select(lambda c: c.name is category)
        cats = list(q)
        expenses = list(Expense.select().order_by(Expense.id))
        expense = expenses[row]

        if len(cats) == 1:
            cat = cats[0]
            expense.category = cat

        expense.expense_date = expense_date
        expense.amount = amount
        expense.comment = comment
        commit()
    except Exception as e:
        print(e)


@db_session
def delete_expense(row):
    try:
        expenses = list(Expense.select().order_by(Expense.id))
        expense = expenses[row]
        expense.delete()

        commit()
    except Exception as e:
        print(e)


@db_session
def add_category(name):
    try:
        q = Category.select(lambda c: c.name is name)
        cats = list(q)
        if len(cats) == 0:
            Category(name=name)
        else:
            print("There is category with the name", name, "already")
    except Exception as e:
        print(e)


@db_session
def get_category():
    try:
        q = Category.select(lambda c: c.name is not None)
        cats = list(q)

        return tuple("".join(cat.name) for cat in cats)
    except Exception as e:
        print(e)


@db_session
def delete_category(name): #TODO: try pony cascase delete
    try:
        cat = Category.get(name=name)
        if cat is not None:
            Expense.select(lambda e: e in cat.expenses).delete(bulk=True)
            cat.delete()
            commit()
    except Exception as e:
        print(e)


@db_session
def update_category(prev_name, new_name):
    try:
        cat = Category.get(name=prev_name)
        cat_alt = Category.get(name=new_name)
        if cat is not None and cat_alt is None:
            cat.name = new_name
            commit()
    except Exception as e:
        print(e)
