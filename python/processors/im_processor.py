import xml.etree.ElementTree as ET
import logging
import json
from sym_api_client_python.processors.message_formatter import MessageFormatter
from sym_api_client_python.processors.sym_message_parser import SymMessageParser
from listeners.expense_approval_form.expense_approval_class import ExpenseReport, render_expense_approval_form, remove_item
from .img_processor import parse_attachment
from .data_service_processor import DataService
from messages.messages import help_message, clear_message, create_message

class IMProcessor:
    def __init__(self, bot_client):
        self.bot_client = bot_client
        self.bot_id = '349026222344891'
        self.sym_message_parser = SymMessageParser()
        self.data_service = DataService()

    def user_has_active_expense(self, streamId, userObj):
        print(userObj['userId'])
        if self.data_service.has_active_expense_report(userObj['userId']):
            self.bot_client.get_message_client().send_msg(streamId, MessageFormatter().format_message('you already have an active expense report, type "@expenseBot end" before starting a new one'))
            return True
        else:
            return False

    def handle_create_expense(self, streamId, userObj):
        if self.user_has_active_expense(streamId, userObj):
            return
        else:
            logging.debug('new expense report requested by {}'.format(userObj['displayName']))
            self.bot_client.get_message_client().send_msg(streamId, create_message)

    #reads message and processes it
    #look inside logs/example.log to see the payload (metadata representing event coming over the datafeed)
    def process(self, msg):
        logging.debug('im_processor/process_im_message()')
        logging.debug(json.dumps(msg, indent=4))

        userId = msg['user']['userId']
        mentioned_users = self.sym_message_parser.get_mention_ids(msg)
        commands = self.sym_message_parser.get_text(msg)

        if mentioned_users:
            if mentioned_users[0] == self.bot_id and commands[0] == 'clear':
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], clear_message)

            elif mentioned_users[0] == self.bot_id and commands[0] == 'create' and commands[1] == 'new':
                self.handle_create_expense(msg['stream']['streamId'], msg['user'])

            # elif mentioned_users[0] == self.bot_id and commands[0] == 'upload' and commands[1] == 'receipt':
            #     upload_expense(parse_attachment(msg, self.bot_client))
            #     self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], render_expense_approval_form('listeners/expense_approval_form/html/create_expense_approval_form.html'))

            elif mentioned_users[0] == self.bot_id and commands[0] == 'end':
                #query database and delete report
                expenses = ExpenseReport.objects(owner=str(userId))
                expenses.delete()
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], MessageFormatter().format_message('type @ExpenseBot create new'))

            else:
                self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], help_message)

        else:
            self.bot_client.get_message_client().send_msg(msg['stream']['streamId'], help_message)
