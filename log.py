import logging
import slack
from logging import handlers
from os import getenv
from json import load


# Note, Stream handler in logging, rotating file handler in handlers
class SlackHandler(logging.StreamHandler):
    def __init__(self, channel, client):
        logging.StreamHandler.__init__(self)
        self.client = client
        self.channel = channel

        response = self.client.chat_postMessage(text=":satellite_antenna: *Starting " + __name__ + "*.....", channel=(self.channel))
        assert response["ok"]

    def emit(self, record):
        msg = self.format(record).replace("CRITICAL -", "CRITICAL - <!channel>")
        response = self.client.chat_postMessage(text=msg, channel=(self.channel))
        assert response["ok"]


def new_handler(handler_type, level, format="*%(filename)s :* %(levelname)s - %(message)s"):
    handler_type.setLevel(level)
    handler_type.setFormatter(logging.Formatter(format))
    logbject.addHandler(handler_type)


# Load config
with open("/".join(__file__.split("/")[:-1]) + "/config.json") as f:
    config = load(f)

# Start slack webclient.
client = slack.WebClient(token=config["api_token"])

# Init log object
logbject = logging.getLogger(__name__)
logbject.setLevel(logging.DEBUG)
# console_handler sends to stdout
new_handler(logging.StreamHandler(), getenv("LOGLEVEL", "INFO"), format="%(levelname)s - %(message)s")

# file_handler appends to designated file
new_handler(handlers.RotatingFileHandler(config["path"], maxBytes=5000000, backupCount=1), "WARNING")

# slack_handler sends to slack channel.
if getenv("TEST", "") == "TRUE":
    slack_channel = config["test_slack_channel"]
else:
    slack_channel = config["slack_channel"]

new_handler(SlackHandler(slack_channel, client), "WARNING")