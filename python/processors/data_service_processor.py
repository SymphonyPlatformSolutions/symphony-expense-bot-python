from listeners.expense_approval_form.expense_approval_class import ExpenseReport

class DataService:
    def __init__(self):
        pass

    def has_active_expense_report(self, userId):
        expenses = ExpenseReport.objects(owner=str(userId), open=True)
        if expenses:
            print('data service', expenses)
            return True
        else:
            print('no expense reports are open, continue')
            return False
