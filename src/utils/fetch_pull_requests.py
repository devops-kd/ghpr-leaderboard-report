'''
This module fetches the pull request based on the 
provided repository name and github personal access
token, processes it and returns a summary of open,
merged and closed prs as dict object of list.
'''

from datetime import datetime, timedelta, timezone
from github import Github


def get_last_week_date():
    '''
    This function that returns the last week date.
    The returned values will be used to filter queried
    pull requests.
    '''
    return datetime.now(timezone.utc)  - timedelta(days=7)


def get_pull_request_api(repo_name, token, state):
    '''
    This function that performs the send request to the github repo using
    PyGithub api. The retun value of this method will list of 
    pull requests from the repo name passed as a parameter

    Parameters:
    repo_name(str): The name of the repo you want to fetch pull request.
                    eg., 'devops-kd/ghpr-leaderboard-report'
    token(str)    : Github Personal Access token for authentication
    state(str)    : Status of the pull requests, eg., open | merged | closed

    Usage: get_pull_request_api('devops-kd/ghpr-leaderboard-report',
                                'gh_123456abcdefg',
                                'all')

    '''
    github = Github(token)
    repo = github.get_repo(repo_name)
    pull_requests = repo.get_pulls(state=state, sort='created', direction='desc')
    return pull_requests


def fetch_pull_requests(repo_name, token):
    '''
    This is the primary function that calls the get_pull_request_api
    method, filters the returned pull request data with last_week_date, status 
    returns a dict object as a value for further processing.
    '''
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
