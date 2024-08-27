'''
Main module of the entire solution that executes methods in sequence to fetch, 
process, render and send generated report.
'''
import os
from utils import fetch_pull_requests
from utils import generate_report
from utils import slack


token = os.environ['GITHUB_TOKEN']
repo_name = os.environ['REPO_NAME']
summary = fetch_pull_requests.fetch_pull_requests(repo_name, token, 7)
print(type(summary))
report = generate_report.generate_report_from_j2_template(summary)
print(type(report))
slack.send_slack_message(report)
