import jinja2
import json
import pprint

from mongoengine import *
connect('expenses')

from jinja2 import Template
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser

class ExpenseReport(Document):
    expenses = ListField(required=True)
    owner = StringField(required=True)
    username = StringField(required=True)
    report_total = IntField(default=0)
    open = BooleanField(default=True)
    manager = StringField(default='')

# expenses = ExpenseReport.objects.delete()

def save_expense(bot_client, action, expense):
    user_id = SymElementsParser().get_initiator_user_id(action)
    username = SymElementsParser().get_initiator_display_name(action)
    for name, date, price, description in expense:
        try:
            expense = ExpenseReport.objects(owner=str(user_id), open=True)
            count = ExpenseReport.objects.count()
            if expense:
                total = float(expense[0]['report_total'])
                total += float(price)
                print(total)
                expense.update(report_total=total)
                expense.update(push__expenses=dict(expense_name = name, expense_date = date, expense_price = float(price), expense_description = description))
                print(expense.to_json())
            else:
                newExpense = ExpenseReport(expenses=[dict(expense_name = name, expense_date = date, expense_price = float(price), expense_description = description)],
                owner=str(user_id), username=username, report_total=int(price), open=True).save()
        except ValueError:
            print('retry with price as a number')

def remove_item(expense_index):
    item_price = float(expense_data['ExpenseApprovalForm']['expenses'][expense_index]['expense_price'])
    expense_data['ExpenseApprovalForm']['report_total'] -= item_price
    del expense_data['ExpenseApprovalForm']['expenses'][expense_index]

def render_expense_approval_form(action, path_to_html_form):
    user_id = SymElementsParser().get_initiator_user_id(action)
    expense_data = ExpenseReport.objects(owner=str(user_id), open=True)
    expense_data = {
        "ExpenseApprovalForm": {
            "username": expense_data[0]['username'],
            "expenses": expense_data[0]['expenses'],
            "person_name": expense_data[0]['owner'],
            "report_total": expense_data[0]['report_total'],
            "user_id" : str(user_id)
        }
    }
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_add_expense_form(action, path_to_html_form):
    user_id = SymElementsParser().get_initiator_user_id(action)
    expense_data = ExpenseReport.objects(owner=str(user_id), open=True)
    if len(expense_data) == 0:
        print('no expenses yet')
        expense_data = {
            "ExpenseApprovalForm": {
                "expenses": [
                ]
            }
        }
        with open(path_to_html_form) as file:
            template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
        html = template.render(expense_data)
        return dict(message = html)
    else:
        expense_data = {
            "ExpenseApprovalForm": {
                "expenses": expense_data[0]['expenses'],
                "person_name": expense_data[0]['owner'],
                "report_total": expense_data[0]['report_total']
            }
        }
        with open(path_to_html_form) as file:
            template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
        html = template.render(expense_data)
        return dict(message = html)

def render_remove_expense_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_select_boss_form(action, path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render()
    return dict(message = html)

def render_select_finance_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render()
    return dict(message = html)
