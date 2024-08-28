# ghpr-leaderboard-report 

## Welcome to the Github Pull request Leader Board Report!

The sole purpose of this project is to generate a simple user friendly report on a github repo pull request for the given no. of days. It primarily sends out a notification to the slack channel with Opened, Merged and Closed pull request data within the last week by default. You can further go back and fetch more data by explicitly mentioning `--days` flag in the command line.

The entire solution is built with python and jinja2 library.

**Python Version used for development:**
* Python 3.10.12

**Required Python Libraries:**
* PyGithub
* jinja2

**Required Arguments:**
* *GH_ACCESS_TOKEN* - Set you github personal access token as an environment variable 
    `export GH_ACCESS_TOKEN=<your_gh_PAT>`
* *SLACK_WEBHOOK_URL* - Set your team slack channel webhook url as an environment variable
    `export SLACK_WEBHOOK_URL='https://<your_webjook_url>'`
* *repoName* - This is a command line argument to pass your repository name, if you do not pass this will not work. `--repoName your-org/your-repo-name`
* *days (optional)* - By default it will fetch data from a week ago(7 days ago from now). This is a command line argument to go further back in dates to fetch Pull requests beyond last week. 
    ```bash
    # This will fetch data 15 days ago from now

    --days 15 
    ```

## Usage

Let us explore how to use this solution.

### Run Docker image

This project has already created a dokcer image `ghpr-leaderboard-report`. You pull the image in your local and run the docker image to generate and send the report to your slack channel.

```bash
# Pull the docker image from the public registry

docker pull karthi211187/ghpr-leaderboard-report:v0.1.0

# Run the doker image to execute the script which will
# fetch the pull requests, process them and send it to slack channel.

docker run -d -e GH_ACCESS_TOKEN=$GH_ACCESS_TOKEN \
            -e SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL \
            --name ghpr-leaderboard-report \
            ghpr-leaderboard-report:v0.1.0 --repoName jekyll/jekyll --days 30
```

### Installation steps for local development

Let us explore the steps to install and run it in your local.

```bash
git clone git@github.com:devops-kd/ghpr-leaderboard-report.git

cd ghpr-leaderboard-report/src

export GH_ACCESS_TOKEN='Your token'
export SLACK_WEBHOOK_URL='your_slak_webhook_url'

pip3 install -r requirements.txt

python3 main.py --repoName jekyll/jekyll --days 7 # --days flag is optional

```

