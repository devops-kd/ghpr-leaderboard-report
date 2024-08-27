from github import Github
from datetime import datetime, timedelta, timezone
import os


def get_last_week_date():
    return datetime.now(timezone.utc)  - timedelta(days=7)


def get_pull_request_api(repo_name, token, state):
    github = Github(token)
    repo = github.get_repo(repo_name)
    pull_requests = repo.get_pulls(state=state, sort='created', direction='desc')
    return pull_requests
    

def fetch_pull_requests(repo_name, token):
    last_week_date = get_last_week_date()
    summary = {'opened': [], 'merged': [], 'closed': []}
    pull_requests = get_pull_request_api(repo_name, token, "all")
    for pr in pull_requests:
        if pr.is_merged() and pr.merged_at > last_week_date:
            summary['merged'].append(pr)
        elif pr.state == 'open' and pr.created_at > last_week_date:
            summary['opened'].append(pr)
        elif pr.state == 'closed' and pr.closed_at > last_week_date:
            summary['closed'].append(pr)
    return summary