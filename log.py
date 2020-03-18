import logging, slack
from os import getenv
from json import load

class SlackHandler(logging.StreamHandler):
    def __init__(self, channel, client):
        logging.StreamHandler.__init__(self)
        self.client = client
        self.channel = channel
        
        response=self.client.chat_postMessage(
            text=":satellite_antenna: Starting up new logger...",
            channel=(self.channel)
        )
        assert response["ok"]

    def emit(self, record):
        msg = self.format(record).replace("WARNING -", ":warning:").replace("ERROR -", ":x:")
        response=self.client.chat_postMessage(
            text=msg,
            channel=(self.channel)
        )
        assert response["ok"]

def new_handler(handler_type, level, format="*%(filename)s :* %(levelname)s - %(message)s"):
    handler_type.setLevel(level)
    handler_type.setFormatter(logging.Formatter(format))
    logbject.addHandler(handler_type)
    print(handler_type)

# Load config
with open("/".join(__file__.split('/')[:-1]) + '/config.json') as f:
    config = load(f)

# Start slack webclient.
client = slack.WebClient(token=config["api_token"])

# Init log object
logbject = logging.getLogger(__name__)
logbject.setLevel(logging.DEBUG)
# console_handler sends to stdout
new_handler(logging.StreamHandler(), getenv("LOGLEVEL", "INFO"), format="%(levelname)s - %(message)s")

# file_handler appends to designated file
new_handler(logging.FileHandler(config["path"]), "WARNING")

# slack_handler sends to slack channel.
new_handler(SlackHandler(config["channel"], client), "WARNING")



