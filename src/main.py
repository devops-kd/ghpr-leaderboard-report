'''
Main module of the entire solution that executes methods in sequence to fetch, 
process, render and send generated report.
'''
import os
import argparse
from utils import fetch_pull_requests
from utils import generate_report
from utils import slack


parser = argparse.ArgumentParser(description='ghpr-leaderboard')
parser.add_argument('--repoName', default="devops-kd/terraform-az-104")
parser.add_argument('--days', default="7")
parser.add_argument('--ghPAT', default="")
args = parser.parse_args()


token = os.environ['GH_ACCESS_TOKEN'] if args.ghPAT == "" else args.ghPAT
repo_name = os.environ['REPO_NAME'] if args.repoName == "" else args.repoName
NUM_OF_DAYS = 7 if args.days == "" else int(args.days)
summary = fetch_pull_requests.fetch_pull_requests(repo_name, token, NUM_OF_DAYS)
report = generate_report.generate_report_from_j2_template(summary)
slack.send_slack_message(report)
