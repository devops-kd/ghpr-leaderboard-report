from github import Github
from datetime import datetime, timedelta, timezone

def fetch_pull_requests(repo_name, token):
    github = Github(token)
    repo = github.get_repo(repo_name)
    last_week_date = datetime.now(timezone.utc)  - timedelta(days=7)
    pull_requests = repo.get_pulls(state='all', sort='created', direction='desc')
    summary = {'opened': [], 'merged': [], 'closed': []}
    for pr in pull_requests:
        if pr.created_at > last_week_date:
            pr_data = {
                'title': pr.title,
                'url': pr.html_url,
                'created_at': pr.created_at,
                'updated_at': pr.updated_at,
                'merged_by': pr.merged_by, 
                'user': pr.user,
                'state': pr.state
            }
            if pr.is_merged():
                summary['merged'].append(pr_data)
            elif pr.state == 'open':
                summary['opened'].append(pr_data)
            elif pr.state == 'closed':
                summary['closed'].append(pr_data)
    return summary