'''
This module fetches the pull request based on the 
provided repository name and github personal access
token, processes it and returns a summary of open,
merged and closed prs as dict object of list.
'''

from datetime import datetime, timedelta, timezone
from github import Github


def get_last_week_date(num_of_days_ago):
    '''
    This function returns the last week date.
    The returned value will be used to filter queried
    pull requests for further processing.

    Parameters:
    num_of_days_ago(int): Integer value that represents no. of days ago, since when to fetch the PR data.
                          Default value should be 7 days, it can be configured older than that.

    Return type: datetime.datetime
    '''
    return datetime.now(timezone.utc) - timedelta(days=int(num_of_days_ago))


def get_pull_request_api(repo_name, start_date, github ):
    '''
    This function that performs the send request to the github repo using
    PyGithub api. The retun value of this method will list of 
    pull requests from the repo name passed as a parameter

    Parameters:
    repo(github.Repository.Repository): Object of the github.Repository.Repository
    state(str)    : Status of the pull requests, eg., open | merged | closed

    Return type: PaginatedList of github.Issues.Issue
    '''
    start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    query = f'repo:{repo_name} is:pr updated:>={start_date_str}'
    return github.search_issues(query)

def fetch_pull_requests(repo_name, token, num_of_days_ago):
    '''
    This is the primary function that calls the get_pull_request_api()
    method, filters the returned pull request data with last_week_date and status 
    returns a dict object with list of opened, merged and closed PR created 
    in the last week for further processing.

    Parameters:
    repo_name(str)      : The name of the repo you want to fetch pull request.
                          eg., 'devops-kd/ghpr-leaderboard-report'
    token(str)          : Github Personal Access token for authentication
    num_of_days_ago(int): Integer value that represents no. of days ago to fetch the PR data.

    Return type: dict
    '''
    last_week_date = get_last_week_date(num_of_days_ago)
    github = Github(token)
    repo = github.get_repo(repo_name)
    summary = {'opened': [], 'merged': [], 'closed': [], 'updated': []}
    issues = get_pull_request_api(repo_name, last_week_date, github)

    for issue in issues:
        if issue.pull_request:
            pr = repo.get_pull(issue.number)
            if pr.is_merged() and pr.merged_at > last_week_date:
                summary['merged'].append(pr)
            elif pr.state == 'open' and pr.created_at > last_week_date:
                summary['opened'].append(pr)
            elif pr.state == 'closed' and pr.closed_at > last_week_date:
                summary['closed'].append(pr)
            elif pr.state == 'open' and pr.updated_at > last_week_date:
                summary['updated'].append(pr)
    return summary
