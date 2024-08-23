from utils import fetch_pull_requests
from utils import generate_report
from utils import slack
import os


# Usage example
token = os.environ['GITHUB_TOKEN']
repo_name = os.environ['REPO_NAME']
summary = fetch_pull_requests.fetch_pull_requests(repo_name, token)
report = generate_report.generate_report(summary)
slack.send_slack_message(report)
