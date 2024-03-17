from pony.orm import *
from bookkeeper.models.entities import Budget


@db_session
def add_budget(monthly, weekly, daily):
    try:
        Budget(daily=daily, weekly=weekly, monthly=monthly)
    except Exception as e:
        print(e)  # TODO: This should be sent to GUI in a user-friendly manner


@db_session
def get_budget():
    try:
        q = Budget.select().order_by(desc(Budget.id)).limit(1)
        budget = q.to_list()[0]
        return tuple([budget.daily, budget.weekly, budget.monthly])  # TODO: return the object itself for GUI?
    except Exception as e:
        print(e)  # TODO: This should be sent to GUI in a user-friendly manner