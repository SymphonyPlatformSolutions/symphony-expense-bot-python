import logging

#Import IMListener class from SDK
#IMListener is an interface
#IMListenerTestImp implements this IMListener Interface
from sym_api_client_python.listeners.elements_listener import ElementsActionListener
from sym_api_client_python.processors.sym_elements_parser import SymElementsParser
#import MessageProcessor class --> parses message/handles functionality
from processors.action_processor import ActionProcessor
from messages.messages import Messages


class ElementsListenerTestImp(ElementsActionListener):
    """Example implementation of IMListener
        sym_bot_client: contains clients which respond to incoming events
    """

    def __init__(self, sym_bot_client):
        self.bot_client = sym_bot_client
        self.bot_id = self.bot_client.bot_id
        self.messages = Messages(self.bot_id)
        self.action_processor = ActionProcessor(self.bot_client)
    def on_elements_action(self, action):
        stream_type = self.bot_client.get_stream_client().stream_info_v2(SymElementsParser().get_stream_id(action))
        if stream_type['streamType']['type'] == 'IM':
            self.action_processor.process_im_action(action)
        elif stream_type['streamType']['type'] == 'ROOM':
            self.bot_client.get_message_client().send_msg(SymElementsParser().get_stream_id(action), self.messages.room_message)
