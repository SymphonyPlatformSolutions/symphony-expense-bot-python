import jinja2
import json
import logging
import os

with open('./environment.json', 'r') as f:
    data = json.load(f)

print(data['db'])
print(data['host'])

# mongoDB configuration
from mongoengine import *
connect(
    db=data['db'],
    host=data['host']
)
print('connecting')

# from mongoengine import *
# connect(
#     db=os.environ['DB'],
#     host=os.environ['HOST']
# )

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

def save_expense(bot_client, action, expense):
    user_id = SymElementsParser().get_initiator_user_id(action)
    username = SymElementsParser().get_initiator_display_name(action)
    for name, date, price, description in expense:
        try:
            expense = ExpenseReport.objects(owner=str(user_id), open=True)
            if expense:
                total = float(expense[0]['report_total'])
                total += float(price)
                expense.update(report_total=total)
                expense.update(push__expenses=dict(expense_name = name, expense_date = date, expense_price = float(price), expense_description = description))
            else:
                newExpense = ExpenseReport(expenses=[dict(expense_name = name, expense_date = date, expense_price = float(price), expense_description = description)],
                owner=str(user_id), username=username, report_total=float(price), open=True).save()
        except ValueError:
            bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), MessageFormatter().format_message('Invalid price format, try again'))

def save_image(bot_client, userId, expense):
    for name, date, price, description in expense:
        try:
            expense = ExpenseReport.objects(owner=str(userId), open=True)
            if expense:
                total = float(expense[0]['report_total'])
                total += float(price)
                expense.update(report_total=total)
                expense.update(push__expenses=dict(expense_name = name, expense_date = date, expense_price = float(price), expense_description = description))
            else:
                newExpense = ExpenseReport(expenses=[dict(expense_name = name, expense_date = date, expense_price = float(price), expense_description = description)],
                owner=str(userId), username=username, report_total=float(price), open=True).save()
        except ValueError:
            bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), MessageFormatter().format_message('Invalid price format, try again'))

def remove_item(action, name, price):
    user_id = SymElementsParser().get_initiator_user_id(action)
    expense = ExpenseReport.objects(owner=str(user_id), open=True)
    total = float(expense[0]['report_total'])
    total -= float(price)
    expense.update(pull__expenses={"expense_name":name}, set__report_total=total)
    logging.debug('updated expense: ', expense.to_json())

def render_expense_approval_form(action, path_to_html_form):
    user_id = SymElementsParser().get_initiator_user_id(action)
    expense_data = ExpenseReport.objects(owner=str(user_id), open=True)
    logging.debug('inside: ', expense_data.to_json())
    if len(expense_data) == 0:
        logging.debug('no expenses yet')
        logging.debug('expense data: ', expense_data)
        expense_data = {
            "ExpenseApprovalForm": {
                "expenses": [
                ]
            }
        }
    else:
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

def render_expense_approval_from_message(userId, path_to_html_form):
    expense_data = ExpenseReport.objects(owner=str(userId), open=True)
    logging.debug('inside: ', expense_data.to_json())
    if len(expense_data) == 0:
        logging.debug('no expenses yet')
        logging.debug('expense data: ', expense_data)
        expense_data = {
            "ExpenseApprovalForm": {
                "expenses": [
                ]
            }
        }
    else:
        expense_data = {
            "ExpenseApprovalForm": {
                "username": expense_data[0]['username'],
                "expenses": expense_data[0]['expenses'],
                "person_name": expense_data[0]['owner'],
                "report_total": expense_data[0]['report_total'],
                "user_id" : str(userId)
            }
        }
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_add_expense_form(action, path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render()
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
