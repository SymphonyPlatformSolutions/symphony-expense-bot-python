from listeners.expense_approval_form.expense_approval_class import ExpenseReport
import logging

class DataService:
    def __init__(self):
        pass

    def has_active_expense_report(self, userId):
        expenses = ExpenseReport.objects(owner=str(userId), open=True)
        if expenses:
            logging.debug('data service', expenses.to_json())
            return True
        else:
            logging.debug('no expense reports are open, continue')
            return False
