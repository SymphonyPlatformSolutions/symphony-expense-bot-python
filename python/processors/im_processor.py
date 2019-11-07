import logging
import json
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.processors.sym_message_parser import SymMessageParser
from listeners.expense_approval_form.expense_approval_class import render_expense_approval_form, render_expense_approval_from_message, render_add_expense_form, render_remove_expense_form, save_expense, save_image, remove_item, render_select_boss_form, render_select_finance_form, ExpenseReport
from .img_processor import parse_attachment
from .data_service_processor import DataService
from messages.messages import Messages

class IMProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.bot_id = self.bot_client.bot_id
        self.messages = Messages(self.bot_id)
        self.sym_message_parser = SymMessageParser()
        self.data_service = DataService()

    def user_has_active_expense(self, streamId, userObj):
        if self.data_service.has_active_expense_report(userObj['userId']):
            self.bot_client.get_message_client().send_msg(streamId, self.messages.end_message)
            return True
        else:
            return False

    def handle_create_expense(self, streamId, userObj):
        if self.user_has_active_expense(streamId, userObj):
            return
        else:
            logging.debug('new expense report requested by {}'.format(userObj['displayName']))
            self.bot_client.get_message_client().send_msg(streamId, self.messages.create_message)

    def process(self, msg):
        logging.debug('im_processor/process_im_message()')
        logging.debug(json.dumps(msg, indent=4))

        userId = msg['user']['userId']
        mentioned_users = self.sym_message_parser.get_mention_ids(msg)
        commands = self.sym_message_parser.get_text(msg)

        if mentioned_users:
            if mentioned_users[0] == self.bot_id and commands[0] == 'clear':
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], self.messages.clear_message)

            elif mentioned_users[0] == self.bot_id and commands[0] == 'create':
                self.handle_create_expense(msg['stream']['streamId'], msg['user'])

            elif mentioned_users[0] == self.bot_id and commands[0] == 'upload' and commands[1] == 'receipt':
                img_data = parse_attachment(msg, self.bot_client)
                print(img_data)
                save_image(self.bot_client, userId, img_data)
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], render_expense_approval_from_message(userId, './listeners/expense_approval_form/html/create_expense_approval_form.html'))

            elif mentioned_users[0] == self.bot_id and commands[0] == 'end':
                expenses = ExpenseReport.objects(owner=str(userId))
                expenses.delete()
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], self.messages.instruction_message)

            else:
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], self.messages.help_message)

        else:
            self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], self.messages.help_message)
