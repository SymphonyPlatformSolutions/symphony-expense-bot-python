import sys
import logging
import json
from pathlib import Path

from sym_api_client_python.configure.configure import SymConfig
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient
from listeners.im_listener_test_imp import IMListenerTestImp
from listeners.element_listener_test_imp import ElementsListenerTestImp

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
    print('In virtual environment. Proceeding.')
else:
    print('Not running in virtual environment. Consider exiting program with ctrl-c')
    print('Docs for setting up virtual environment:')
    print('https://docs.python.org/3/library/venv.html')

def load_env(path_to_env_file):
    with open(path_to_env_file, "r") as env_file:
        data = json.load(env_file)
        if 'bot_id' in data:
            data['bot_id'] = data['bot_id']
    return data

def configure_logging():
        mydir = Path('logs')
        mydir.mkdir(exist_ok=True, parents=True)
        myfname = mydir.joinpath('example.log')
        logging.basicConfig(
                filename='./logs/example.log',
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                filemode='w', level=logging.DEBUG
        )
        logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
        configure_logging()
        configure = SymConfig('./resources/config.json')
        configure.load_config()
        bot_env = load_env('./resources/environment.json')
        auth = SymBotRSAAuth(configure)
        auth.authenticate()
        # Initialize SymBotClient with auth and configure objects
        bot_client = SymBotClient(auth, configure)
        bot_client.bot_id = bot_env['bot_id']
        # Initialize datafeed service
        datafeed_event_service = bot_client.get_datafeed_event_service()
        # Add Listeners to datafeed event service
        im_listener_test = IMListenerTestImp(bot_client)
        datafeed_event_service.add_im_listener(im_listener_test)
        element_listener_test = ElementsListenerTestImp(bot_client)
        datafeed_event_service.add_elements_listener(element_listener_test)
        # Create and read the datafeed
        print('Starting datafeed')
        datafeed_event_service.start_datafeed()

if __name__ == "__main__":
    main()
