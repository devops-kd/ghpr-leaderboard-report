from requests import post
import os
import json

def send_slack_message(message):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    response = post(url=slack_webhook_url, json=message)

    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Failed to send report summary to Slack channel. Status code {response.status_code}")