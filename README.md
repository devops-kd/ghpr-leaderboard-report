# ghpr-leaderboard-report 

- [Introduction](#introduction)
- [Usage](#usage)
- [Options to schedule this regularly](#options-to-schedule-this-regularly)

## Introduction

Welcome to the Github Pull request Leader Board Report!

The sole purpose of this project is to generate a simple user friendly report on a github repo pull request for the given no. of days. It primarily sends out a notification to the slack channel with Opened, Merged and Closed pull request data within the last week by default. You can further go back and fetch more data by explicitly mentioning `--days` flag in the command line.

The entire solution is built with python and jinja2 library.

**Python Version used for development:**
* Python 3.10.12

**Required Python Libraries:**
* PyGithub
* jinja2

**Required Arguments:**
* *GH_ACCESS_TOKEN* - Set you github personal access token (PAT) as an environment variable 
    `export GH_ACCESS_TOKEN=<your_gh_PAT>`
* *SLACK_WEBHOOK_URL* - Set your team slack channel webhook url as an environment variable
    `export SLACK_WEBHOOK_URL='https://<your_webhook_url>'`
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
# Set environment variables
export GH_ACCESS_TOKEN='Your token'
export SLACK_WEBHOOK_URL='your_slack_webhook_url'

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

# Options to schedule this regularly
- [Github Actions](#github-actions)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Kubernetes Manifest](#kubernetes-cronjob)
- [Kubernetes with helm](#kubernetes-cronJob-with-helm)


## GitHub Actions

### Step 1: Create GitHub Actions Workflow
1. Create a `.github/workflows` directory in your repository if it doesn’t exist.
1. Create a new workflow file, e.g., `weekly-report.yml`, in the `.github/workflows` directory.
    ```yaml
    name: Weekly Pull Request Report

    on:
    schedule:
        - cron: '0 23 * * 5'  # Runs at 23:00 UTC every Friday
    
    env:
        GH_ACCESS_TOKEN: ${{ secrets.GH_ACCESS_TOKEN }}
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

    jobs:
        generate-report:
            runs-on: ubuntu-latest
            container:
                image: ghpr-leaderboard-report:v0.1.0
            steps:
            - name: Checkout repository
              uses: actions/checkout@v2

            - name: Run report generation
              run: |
                docker run \
                    -e GH_ACCESS_TOKEN=${{ env.GH_ACCESS_TOKEN }} \
                    -e SLACK_WEBHOOK_URL=${{ env.SLACK_WEBHOOK_URL }} \
                    ghpr-leaderboard-report:v0.1.0 --repoName jekyll/jekyll --days 30
    ```

### Step 2: Set Up Secrets
1. Go to your repository on GitHub.
1. Navigate to `Settings` > `Secrets` > `Actions`.
1. Add a new secret named `GH_ACCESS_TOKEN` with your GitHub personal access token.
1. Add another secret named `SLACK_WEBOOK_URL` with your slack channel webhook.


## Jenkins Pipeline

### Step 1: Create Jenkins Pipeline Job
1. Open Jenkins and create a new Pipeline job.
1. In the Pipeline section, configure the pipeline script.
    ```groovy
    pipeline {
        agent any

        triggers {
            cron('H 23 * * 5')  // Runs at 23:00 every Friday
        }

        stages {
            stage('Checkout') {
                steps {
                    checkout scm
                }
            }

            stage('Run Docker Container') {
                steps {
                    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN'),
                                    string(credentialsId: 'slack-webhook-url', variable: 'URL')]) {
                    script {
                        docker.image('ghpr-leaderboard-report:v0.1.0').inside {
                            sh '''
                            docker run \
                            -e GH_ACCESS_TOKEN=${GITHUB_TOKEN} \
                            -e SLACK_WEBHOOK_URL=${URL} \
                            ghpr-leaderboard-report:v0.1.0 --repoName jekyll/jekyll --days 30
                            '''
                        }
                    }
                }
            }
        }
    }
    ```
1. you can further parameterize the commandline argumments, to execute on demand.

### Step 2: Set Up Credentials
1. Go to Jenkins and navigate to `Manage Jenkins` > `Manage Credentials`.
1. Add a new credential with your `GitHub personal access token` and ID `github-token`.
1. Add a new credential with your `secret-text` and ID `slack-webhook-url`


## Kubernetes CronJob

This guide provides detailed steps to package and deploy the ghpr-leaderboard-report Docker container as a Kubernetes CronJob using Helm. 

### Step 1: Create Kubernetes CronJob
1. Create a Kubernetes CronJob YAML file, e.g., `cronjob.yaml`.
    ```yaml
    apiVersion: batch/v1
    kind: CronJob
    metadata:
    name: ghpr-leaderboard-report
    spec:
    schedule: "0 23 * * 5"  # Runs at 23:00 every Friday
    jobTemplate:
        spec:
        template:
          spec:
            securityContext:
                runAsNonRoot: true
                runAsUser: 1000
            containers:
            - name: ghpr-leaderboard-report
              args:
                - "--repoName"
                - "jekyll/jekyll"
              image: ghpr-leaderboard-report:v0.1.0
              env:
              - name: GH_ACCESS_TOKEN
                valueFrom:
                    secretKeyRef:
                        name: github-token
                        key: token
              - name: SLACK_WEBHOOK_URL
                valueFrom:
                    secretKeyRef:
                        name: slack-webhook-url
                        key: webhookUrl
          restartPolicy: OnFailure
    ```

### Step 2: Create Kubernetes Secret
1. Create a Kubernetes secret for the GitHub token.
    ```bash
    kubectl create secret generic github-token --from-literal=token=your_github_token
    kubectl create secret generic slack-webhook-url --from-literal=webhookUrl=your_url

    ```

### Step 3: Apply the CronJob
1. Apply the CronJob configuration.
    ```yaml
    kubectl apply -f cronjob.yaml
    ```


## Kubernetes CronJob with helm

### Step 1: Create a Helm Chart
1. Initialize a Helm chart:
```bash
helm create ghpr-leaderboard-report
```
2. Modify the `Chart.yaml` file with relevant information.
### Step 2: Define the CronJob in the Helm Chart
1. Create a `cronjob.yaml` template in the `templates` directory:
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{ .Release.Name }}-ghpr-leaderboard-report
  labels:
    app: {{ .Release.Name }}-ghpr-leaderboard-report
spec:
  schedule: "0 23 * * 5"  # Runs at 23:00 every Friday
  jobTemplate:
    spec:
      template:
        spec:
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
          containers:
          - name: ghpr-leaderboard-report
            image: ghpr-leaderboard-report:v0.1.0
            args:
            {{- if .Values.repoName }}
              - "--repoName"
              - {{ .Values.repoName | quote }} 
            {{- end}}
            {{- if .Values.days }}
              - "--days"
              - {{ .Values.days | quote }} 
            {{- end}}
            env:
            - name: GH_ACCESS_TOKEN
              valueFrom:
                secretKeyRef:
                    name: github-token
                    key: token
            - name: SLACK_WEBHOOK_URL
              valueFrom:
                secretKeyRef:
                    name: slack-webhook-url
                    key: webhookUrl
          restartPolicy: OnFailure
```
1. Update `values.yaml` with default values:
```yaml
repoName: "owner/repo"
days: 15 # Default value is 7
```

### Step 3: Create Kubernetes Secret for GitHub Token
1. Create a Kubernetes secret:
    ```bash
    kubectl create secret generic github-token --from-literal=token=your_github_token
    kubectl create secret generic slack-webhook-url --from-literal=webhookUrl=your_url

    ```

### Step 4: Package and Deploy the Helm Chart
1. Package the Helm chart:
```bash
helm package ghpr-leaderboard-report
```

1. Deploy the Helm chart:
```bash
helm install ghpr-leaderboard-report ./ghpr-leaderboard-report
```
