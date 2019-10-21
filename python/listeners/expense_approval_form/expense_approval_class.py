import jinja2
from jinja2 import Template
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser

expense_data = {
    "ExpenseApprovalForm": {
        "expenses": [
        ],
        "person_name": "",
        "report_name": "",
        "report_summary": "",
        "report_total": 0.00
    }
}

def upload_expense(bot_client, action, expense):
    for name, date, price, description in expense:
        try:
            expense_data['ExpenseApprovalForm']['report_total'] += float(price)
            expense_data['ExpenseApprovalForm']['expenses'].append(dict(expense_name = name,
                                                                     expense_date = date,
                                                                     expense_price = float(price),
                                                                     expense_description = description))
        except ValueError:
            print('retry with price as a number')
            bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), MessageFormatter().format_message('submit valid price format'))
def remove_item(expense_index):
    print(expense_index)
    item_price = float(expense_data['ExpenseApprovalForm']['expenses'][expense_index]['expense_price'])
    print(item_price)
    expense_data['ExpenseApprovalForm']['report_total'] -= item_price
    del expense_data['ExpenseApprovalForm']['expenses'][expense_index]

def render_expense_approval_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_add_expense_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_remove_expense_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_select_boss_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)

def render_select_finance_form(path_to_html_form):
    with open(path_to_html_form) as file:
        template = Template(file.read(), trim_blocks=True, lstrip_blocks=True)
    html = template.render(expense_data)
    return dict(message = html)
