"""CRUD controller functions"""
from pony.orm import *
from bookkeeper.models.entities import Budget, Expense, Category
from datetime import date


@db_session
def add_budget(monthly, weekly, daily):
    """add budget to db"""
    try:
        Budget(daily=daily, weekly=weekly, monthly=monthly)
    except Exception as e:
        print(e)


@db_session
def get_budget():
    """get budget data from db and return it"""
    try:
        q = Budget.select().order_by(desc(Budget.id)).limit(1).to_list()
        if len(q):
            budget = q[0]
            return tuple([budget.daily, budget.weekly, budget.monthly])
        else:
            return tuple([0, 0, 0])
    except Exception as e:
        print(e)


@db_session
def add_expense(amount, category):
    """add expense to db"""
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
    """get expense at row from db and return it"""
    try:
        expenses = list(Expense.select().order_by(Expense.id))
        expn = expenses[row]
        return tuple([expn.expense_date, expn.amount, expn.category.name, expn.comment])
    except Exception as e:
        print(e)


@db_session
def get_expense_count():
    """return number of expenses in db"""
    try:
        e = list(Expense.select().order_by(Expense.id))
        return len(e)
    except Exception as e:
        print(e)


@db_session
def update_expense(expense_date, amount, category, comment, row):
    """update info of expense in db"""
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
    """delete expense from db"""
    try:
        expenses = list(Expense.select().order_by(Expense.id))
        expense = expenses[row]
        expense.delete()

        commit()
    except Exception as e:
        print(e)


@db_session
def add_category(name):
    """add category to db"""
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
    """return category from db"""
    try:
        q = Category.select(lambda c: c.name is not None)
        cats = list(q)

        return tuple("".join(cat.name) for cat in cats)
    except Exception as e:
        print(e)


@db_session
def delete_category(name):
    """delete category from db
       delete expenses with same category"""
    try:
        cat = Category.get(name=name)
        if cat is not None:
            Expense.select(lambda d: d in cat.expenses).delete(bulk=True)
            cat.delete()
            commit()
    except Exception as e:
        print(e)


@db_session
def update_category(prev_name, new_name):
    """rename category in db"""
    try:
        cat = Category.get(name=prev_name)
        cat_alt = Category.get(name=new_name)
        if cat is not None and cat_alt is None:
            cat.name = new_name
            commit()
    except Exception as e:
        print(e)


@db_session
def get_expense_sum():
    """return sum of expense amount from db"""
    try:
        expenses = Expense.select()[:]
        sum_day = 0
        sum_week = 0
        sum_month = 0
        for e in expenses:
            if e.expense_date == date.today():
                sum_day += e.amount
            if e.expense_date.month == date.today().month:
                if e.expense_date.year == date.today().year:
                    if date.today().day - e.expense_date.day >= 0:
                        sum_month += e.amount
            if e.expense_date.isocalendar()[1] == date.today().isocalendar()[1]:
                sum_week += e.amount

        return tuple([sum_day, sum_week, sum_month])
    except Exception as e:
        print(e)
