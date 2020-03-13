import os, slack, json, logging

# Settings relative to MODULE no calling script
with open("/".join(__file__.split('/')[:-1]) + '/config.json') as f:
    config = json.load(f)

def init_logger(path):
    # Custom slack handler.
    class SlackHandler(logging.StreamHandler):
        def __init__(self, channel, client):
            logging.StreamHandler.__init__(self)
            self.client = client
            self.channel = channel
            
            response=self.client.chat_postMessage(
                text=":satellite_antenna: Starting up logger...",
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
        # response = client.chat_postMessage(

        #     text="Hello world!")
        # assert response["ok"]
        # assert response["message"]["text"] == "Hello world!"

    # ===== Init Stuff Stuff =====#
    log_path = path
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)



    # Log Info to console USE ENV VARIABLE LOGLEVEL TO OVERRIDE
    console_logs = logging.StreamHandler()
    console_logs.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    try:
        console_logs.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    except Exception as thing:
        console_logs.setLevel("INFO")
    
    log.addHandler(console_logs)

    # Log warnings and above to text file.
    file_logs = logging.FileHandler(log_path)
    file_logs.setLevel("WARNING")
    file_logs.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    log.addHandler(file_logs)

    # Log warnings and above to slack channel.
    # Start slack webclient.

    client = slack.WebClient(token=config["api_token"])
           
    # Target channel
    #channel='#random'
    channel=config["channel"]

    slack_logs = SlackHandler(channel, client)
    slack_logs.setLevel("WARNING")
    slack_logs.setFormatter(logging.Formatter("*%(filename)s :* %(levelname)s - %(message)s"))

    log.addHandler(slack_logs)

    return log

log=init_logger("warn.logs")
