import os, slack, json


with open('config.json') as f:
    config = json.load(f)



client = slack.WebClient(token=config["api_token"])

# response = client.chat_postMessage(

#     text="Hello world!")
# assert response["ok"]
# assert response["message"]["text"] == "Hello world!"

print(config["maintainers"]["callum"])

response=client.chat_postMessage(
#   channel='#random',
    text="Hello world",
    channel=(config["maintainers"]["callum"])
)
assert response["ok"]
