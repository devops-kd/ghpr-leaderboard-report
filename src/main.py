'''
Main module of the entir solution tht executes methos in sequesce to fetch, 
process, render and send report.
'''
import os
from utils import fetch_pull_requests
from utils import generate_report
from utils import slack


token = os.environ['GITHUB_TOKEN']
repo_name = os.environ['REPO_NAME']
summary = fetch_pull_requests.fetch_pull_requests(repo_name, token)
report = generate_report.generate_report_from_j2_template(summary)
slack.send_slack_message(report)
