import logging
import json
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
from listeners.expense_approval_form.expense_approval_class import render_expense_approval_form, render_add_expense_form, render_remove_expense_form, save_expense, remove_item, render_select_boss_form, render_select_finance_form, ExpenseReport
from messages.messages import reply_message, manager_submit_message, start_report_message, choose_boss_message, review_message, finance_approval_message, reject_message

class ActionProcessor:

    def __init__(self, bot_client):
        self.bot_client = bot_client

    def process_im_action(self, action):
        logging.debug('action_processor/im_process')
        logging.debug(json.dumps(action, indent=4))
        if SymElementsParser().get_form_values(action)['action'] == 'create-report':
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), render_add_expense_form(action, 'listeners/expense_approval_form/html/create_expense_approval_form.html'))

        elif SymElementsParser().get_form_values(action)['action'] == 'add-expense-form':
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), render_add_expense_form(action, 'listeners/expense_approval_form/html/add_expense_form.html'))

        elif SymElementsParser().get_form_values(action)['action'] == 'add-expense-button':
            form_contents = SymElementsParser().get_form_values(action)
            save_expense(self.bot_client, action, [(form_contents['add-vendor-textfield'], form_contents['add-date-textfield'], form_contents['add-price-textfield'], form_contents['add-description'])])
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), render_expense_approval_form(action, 'listeners/expense_approval_form/html/create_expense_approval_form.html'))

        elif SymElementsParser().get_form_values(action)['action'] == 'approve':
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), choose_boss_message)
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), render_select_boss_form(action, 'listeners/expense_approval_form/html/select_boss.html'))

        elif SymElementsParser().get_form_values(action)['action'] == 'send-report':
            self.employee_id = SymElementsParser().get_initiator_user_id(action)
            self.employee_name = SymElementsParser().get_initiator_display_name(action)
            self.employee_stream = SymElementsParser().get_stream_id(action)

            self.manager_id = SymElementsParser().get_form_values(action)['person-selector']
            self.manager_username = self.bot_client.get_user_client().get_user_from_id(self.manager_id)['displayName']
            expense = ExpenseReport.objects(owner=str(self.employee_id), open=True)
            expense.update(manager=str(self.manager_id[0]))

            self.submit_message = MessageFormatter().format_message('Your expense has been submitted to {}'.format(self.manager_username) + ' I will inform you when your manager answers')
            self.manager_recieve_message = dict(message = """<messageML>
                                                        <span><p>Hey <mention uid="{}"/>, you have one expense report from <mention uid="{}"/> </p></span>
                                                   </messageML>""".format(self.manager_id[0], self.employee_id))

            self.bot_client.get_message_client().send_msg(self.employee_stream, self.submit_message)
            self.im_stream = self.bot_client.get_stream_client().create_im(SymElementsParser().get_form_values(action)['person-selector'])

            self.bot_client.get_message_client().send_msg(self.im_stream['id'], self.manager_recieve_message)
            self.bot_client.get_message_client().send_msg(self.im_stream['id'], review_message)
            self.bot_client.get_message_client().send_msg(self.im_stream['id'], render_expense_approval_form(action, 'listeners/expense_approval_form/html/manager_expense_approval_form.html'))

        elif SymElementsParser().get_form_values(action)['action'].startswith('approve-expense'):
            user_id = SymElementsParser().get_form_values(action)['action'].split()[1]
            self.manager_stream = SymElementsParser().get_stream_id(action)
            self.bot_client.get_message_client().send_msg(self.manager_stream, manager_submit_message)
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), render_select_finance_form('listeners/expense_approval_form/html/select_finance.html'))

            #query the database and set open=False, find the userID of employee not manager
            expense = ExpenseReport.objects(open=True, owner=str(user_id), manager=str(self.manager_id[0]))[0]
            print(expense.to_json())
            expense.open=False
            expense.save()
            print(expense.to_json())

        elif SymElementsParser().get_form_values(action)['action'] == 'send-finance':
            self.finance_id = SymElementsParser().get_form_values(action)['person-selector']
            self.send_finance_message = dict(message = """<messageML>
                                                        <span><p>Thanks, I'll share this with <mention uid="{}"/>, and send your answer to <mention uid="349026222344902"/> </p></span>
                                                   </messageML>""".format(self.finance_id[0]))
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), self.send_finance_message)

            self.bot_client.get_message_client().send_msg(self.employee_stream, finance_approval_message)

        elif SymElementsParser().get_form_values(action)['action'].startswith('remove'):
            expense_number = int(SymElementsParser().get_form_values(action)['action'][-1])
            remove_item(expense_number)
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), render_expense_approval_form(action, 'listeners/expense_approval_form/html/create_expense_approval_form.html'))

        elif SymElementsParser().get_form_values(action)['action'] == 'reject-expense':
            self.bot_client.get_message_client().send_msg(self.employee_stream, reject_message)
