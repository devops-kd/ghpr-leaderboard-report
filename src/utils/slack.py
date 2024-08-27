'''
The module that sends the generated report  to a slack channel using SLACK_WEBHOOK_URL.
'''

import os
import requests


def send_slack_message(message):
    '''
    This function receives the generated report as json str object and sends a post request
    to the slack channel webhook url.

    Parameters:
    message(str): Json string that contains formatted slack message to be sent to the slack channel
    '''
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    try:
        response = requests.post(url=slack_webhook_url,
                    json=message,
                    timeout=30)
        response.raise_for_status()

    except requests.exceptions.HTTPError as err:
        if response.status_code != 200:
            raise SystemExit(f"Status code: {response.status_code}\nError: {err}") from err
    