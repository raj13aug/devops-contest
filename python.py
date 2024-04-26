0
Jump to Comments
4
Save

Cover image for 🦊 GitLab: A Python Script Calculating DORA Metrics
Zenika profile imageBenoit COUETIL 💫
Benoit COUETIL 💫 for Zenika
Posted on 6 Apr


3

1

2

2

2
🦊 GitLab: A Python Script Calculating DORA Metrics
#
gitlab
#
devops
#
accelerate
#
dora
Initial thoughts
Considered alternate solutions
GitLab Value Stream Analytics (official solution)
LinearB (SaaS solution with free tier)
Four Keys (open source based on GCP)
DORA Metrics and calculations insights
Metric A: Lead Time for Changes
Metric B: Deployment Frequency
Metric C: Change Failure Rate
Metric D: Time to Restore Service
The Python script
Output example
Pre-requisites
Source code
Wrapping up
Further reading
Initial thoughts
The DevOps Research and Assessment (DORA) team has identified four crucial metrics for measuring DevOps performance. Employing these metrics not only enhances DevOps efficiency but also effectively communicates performance to business stakeholders, thereby accelerating business results.

In his insightful article, DORA Metrics: What are they, and what's new in 2024?, Justin Reock provides a comprehensive overview of these metrics. By the way, you should also check out the follow-up article, Developer Experience is Dead: Long Live Developer Experience! 🤓

Embracing DORA program findings, we performed some research on how to obtain these crucial metrics for GitLab projects. The culmination of our exploration is a homemade Python script designed to calculate these metrics for individual projects or an entire group within GitLab, recursively. While the script doesn't generate graphical representations, it serves as a practical tool for periodic metric calculations:

python-output

This script has been executed on a couple of projects and groups across different organizations, yielding interesting results and with little to no effort on the targeted codebase.

Let's now look into the available solutions for GitLab projects, how GitLab officially compute these metrics, and understand the specific metrics our script calculates.

Considered alternate solutions
Some alternate solutions have been explored before making a script from scratch.

GitLab Value Stream Analytics (official solution)
GitLab official DORA metrics in Value Stream Analytics is a wonderful way to display the metrics overtime, without much effort.

gitlab-dora-screenshot

Regrettably, it is exclusively accessible with the Ultimate license level priced at $99 per developer per month. While it certainly brings value, it may be difficult to convince managers to upgrade to this level.

LinearB (SaaS solution with free tier)
linearb-dora-screenshot

LinearB is a SaaS solution that retrieves metrics overtime, some of them being used to calculate DORA Metrics. They also have a Youtube channel that advocate for DORA Metrics and more.

The DORA segment is free, and you should certainly explore it while evaluating solutions in this field.

Four Keys (open source based on GCP)
Four Keys is an open source alternative by Google employees that has been halted earlier this year (but forks-friendly).

fourkeys-dora-dashboard

This is a complete solution that needs a complex set of GCP resources to store and query the data.

fourkeys-dora-design

But we deemed the initial cost too high for initiating DORA Metrics calculation.

a humanoid fox from behind watching metrics dashboards, multiple computer monitors,manga style

DORA Metrics and calculations insights
We found above existing solutions often had drawbacks, like costs or complex setups. So, to keep things simple and flexible, we built our own tool.

We'll dig into the thinking behind our choice, examining the details of GitLab's official metrics calculations. We'll point out any quirks or limitations and introduce our alternative methods.

We'll break down the four key DORA metrics—Lead Time for Changes, Deployment Frequency, Change Failure Rate, and Time to Restore Service. For each one, we'll compare GitLab's way with ours, making it easy for you to grasp how to get these metrics practically.

Metric A: Lead Time for Changes
Lead Time for Changes: How long does it take to go from code committed to code successfully running in production?

GitLab official calculation
How Lead Time for Changes is calculated in GitLab DORA Metrics:

GitLab calculates lead time for changes based on the number of seconds to successfully deliver a commit into production: from merge request merge time (when the merge button is clicked) to code successfully running in production, without adding the coding_time to the calculation. Data is aggregated right after the deployment is finished, with a slight delay.

OK, so if a commit has been pushed 2 weeks ago, and we merged an hour ago, and then we deploy to production, the commit age is one hour ? It does not seem quite right.

By default, lead time for changes supports measuring only one branch operation with multiple deployment jobs (for example, from development to staging to production on the default branch). When a merge request gets merged on staging, and then on production, GitLab interprets them as two deployed merge requests, not one.

This is hard to understand, so what is the LTfC for this commit ? Does it contribute 2 times to the average ? And what about the branch name ? Is it configurable ? The verified branch is main or production ?

Our calculation
Our calculation is fairly simple: the average age of commits deployed to production, created after the last successful deployment to production. Excluding merge commits.

The branch names checked are main and master by default, configurable with a regex.

Metric B: Deployment Frequency
Deployment Frequency: How often does your organization deploy code to production or release it to end users?

GitLab official calculation
How Deployment Frequency is calculated in GitLab DORA Metrics:

In GitLab, deployment frequency is measured by the average number of deployments per day to a given environment, based on the deployment’s end time (its finished_at property). GitLab calculates the deployment frequency from the number of finished deployments on the given day. Only successful deployments (Deployment.statuses = success) are counted.

This makes sense. But it takes into account bug fixes as valid deployments. If we deploy one feature a week and then deploy fixes everyday until the feature works, are we deploying once a day ? It is debatable, but we do not think so.

The calculation takes into account the production environment tier or the environments named production/prod. The environment must be part of the production deployment tier for its deployment information to appear on the graphs.

The environment tier is a nice generic solution. production / prod environment names alternatives are simple and efficient, but will not fit every projects without some change.

Our calculation
We chose to discard deployments of hotfixes. For now this is simple, even simplistic: if the last commit message starts with Merge branch 'hotfix, it is considered a hotfix, then it is not a feature deployment. Later versions of the script could involve regular expression.

For environment names, tier is not taken into account (yet), but a regular expression is used to accommodate to most situations without impacting legacy projects. Default regular expression is every environment starting with "prod", within a subfolder or not ((|.*\/)prod.*). We have to be careful not to include preprod environments.

Metric C: Change Failure Rate
Change Failure Rate: What percentage of changes to production or released to users result in degraded service (e.g., lead to service impairment or service outage) and subsequently require remediation (e.g., require a hotfix, rollback, fix forward, patch)?

GitLab official calculation
Change Failure Rate is calculated in GitLab DORA Metrics:

In GitLab, change failure rate is measured as the percentage of deployments that cause an incident in production in the given time period. GitLab calculates this as the number of incidents divided by the number of deployments to a production environment. This assumes:

GitLab incidents are tracked.
All incidents are related to a production environment.
Incidents and deployments have a strictly one-to-one relationship. An incident is related to only one production deployment, and any production deployment is related to no more than one incident.
Again, a smart solution for a problem involving something beyond the code: detecting an incident. This presupposes several factors; however, achieving precise accuracy is challenging.

Our alternative metric calculation: Ratio of Deployments Needing Hotfix(es)
The accuracy with just calculation is challenging. We chose not to involve ticket management, for now.

Instead, we compute the average Ratio of Deployments Needing Hotfix. If a hotfix has been performed after a deployment, we consider the deployment resulted in degraded service. While this calculation is not the complete metric, it offers a technical and easily measurable insight.

As for another metric, if the last commit message starts with Merge branch 'hotfix, it is considered a hotfix on the previously non-hotfix deployment.

Metric D: Time to Restore Service
Time to Restore Service: How long does it generally take to restore service when a service incident or a defect that impacts users occurs (e.g., unplanned outage, service impairment)?

GitLab official calculation
Time to Restore Service is calculated in GitLab DORA Metrics:

In GitLab, time to restore service is measured as the median time an incident was open for on a production environment. GitLab calculates the number of seconds an incident was open on a production environment in the given time period. This assumes:

GitLab incidents are tracked.
All incidents are related to a production environment.
Incidents and deployments have a strictly one-to-one relationship. An incident is related to only one production deployment, and any production deployment is related to no more than one incident.
A smart solution for a problem involving something beyond the code: detecting an incident. This assumes a lot of things though; The accuracy is challenging.

Our alternative metric calculation: Last Hotfix Median Delay
Again, the accuracy with just calculation is just too challenging. We chose not to involve ticket management.

Instead, we compute the Last Hotfix Median Delay. If there is a hotfix one week after the last successful non-hotfix deployment, it is considered something needed from day one, as a fair approximation. This is not the full compute of the metric, hence not a DORA metric per se, but something technical and easily mesurable.

As for another metric, if the last commit message starts with Merge branch 'hotfix, it is considered a hotfix on the previously non-hotfix deployment.

a humanoid fox from behind watching metrics dashboards, multiple computer monitors,manga style

The Python script
This Python script calculates data for an individual project, a list of projects, or projects within a group recursively, over a specified time span. It doesn't generate graphs or tables; its purpose is straightforward, allowing occasional metric calculations.

Additionally, it serves as an auditing tool, designed to work seamlessly across various project types without requiring modifications.

The script's header provides detailed descriptions of the available arguments.

Output example
python compute-dora-metrics.py --token $GITLAB_TOKEN --group-id 10000 --days 180
python-output

Pre-requisites
Some Python packages installed
pip install requests ansicolors
An access to all the projects in the group
Hotfixes are performed by branches whose name starts with 'hotfix', and merges are performed with a merge commit.
Deployments are performed using the environment feature, and the production environments are distinguished by a common regex.
Source code
"""
GitLab Dora Metrics Calculator for a project or all projects in a group

This script is designed to calculate key DORA (DevOps Research and Assessment) metrics for GitLab projects and groups.

The metrics and their computation include:
- DORA Deployment Frequency:
    - Measures how often code is deployed to production
    - Computed by counting the number of deployments of features (except hotfixes) to the production environment in a specified time period.
- DORA Lead Time for Changes:
    - Measures the time it takes for code changes to go from commit to deployment
    - Computed as the average time between feature commits (excluding merge commits and hotfixes) and their subsequent deployments.
- Deployments Needing Hotfix:
    - Measures the percentage of deployments that require additional hotfixes.
    - Computed by comparing the number of deployments that required a later hotfix to the total number of deployments of features.
- Time to Last Hotfix:
    - Measures how long it takes to hotfix the service after a deployment.
    - Computed as the average time between hotfix deployments and their associated feature deployments.

Prerequisites:
- pip install requests ansicolors
- An access to all the projects in the group
- Hotfixes are performed by branches whose name starts with 'hotfix', and merges are performed with a merge commit.
- Deployments are performed using the environment feature, and the production environments are distinguished by a common regex.

Usage:
python compute-dora-metrics.py --token <token> --days <nb_days> --group-id <group_id>
python compute-dora-metrics.py --token <token> --days <nb_days> --project-ids <project_id1>,<project_id2>,...

Arguments:
  --token          Your GitLab personal access token.
  --gitlab-host    Your GitLab host (default: gitlab.com).
  --group-id       The ID of the GitLab group to analyze.
  --project-ids    Comma-separated list of GitLab project IDs to analyze.
  --days           The duration of analysis in days (default: 90).
  --branch         The main branch (default: main).
  --env            The environment name for production deployments (default: 'prod*', in a subfolder or not).
  --debug          Whether to print more logs (default: false)

Author: Benoit COUETIL
"""

import requests
import argparse
import re
from datetime import datetime, timedelta
from colors import * # COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
from statistics import median

parser = argparse.ArgumentParser(description='Calculate DORA Metrics for a GitLab group and its projects.')
parser.add_argument('--token', required=True, help='Your GitLab personal access token')
parser.add_argument('--gitlab-host', default='gitlab.com', help='Your GitLab host')
parser.add_argument('--group-id', help='The ID of the GitLab group to analyze')
parser.add_argument('--project-ids', help='Comma-separated list of GitLab project IDs to analyze')
parser.add_argument('--branch', default='main|master', help='The main branch')
parser.add_argument('--env', default='(|.*\/)prod.*', help='The prod environment name pattern to match (not search) (default: (|.*\/)prod.*)')
parser.add_argument('--days', type=int, default=90, help='The duration of analysis in days (default 90)')
parser.add_argument("--debug", action=argparse.BooleanOptionalAction, help='Whether to print details of commits (default false)')
args = parser.parse_args()
headers = {'Private-Token': args.token}

def get_available_environments_names(project_id):

    environments_names = []

    params = {
        'per_page': 100,
        'states': 'available',
    }

    any_environment_response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/environments', headers=headers, params=params)
    if any_environment_response.status_code == 200:
        environments = any_environment_response.json()
        if environments:
            for environment in environments:
                environments_names.append(environment['name'])

    return environments_names

# Function to get the last 10 deployments of environment "prod" for a project
def get_last_successful_deployments(project_id, env_name):

    params = {
        'environment': env_name,
        'per_page': 100,
        'order_by': 'updated_at',
        'sort': 'desc',  # Sort in descending order (oldest first)
        'status': 'success',
        'updated_after': updated_after,
    }
    response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/deployments', headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        if args.debug: print(red(response.json()))
        return []

# Function to iterate over deployments and commits
def process_deployments(project_id, env_name, deployments, branch):
    if args.debug: print(f"Processing environment '{magenta(env_name)}'")
    last_commit_date_of_previous_deployment = None
    all_time_differences = []
    deployment_dates = set()  # Collect deployment dates for the project
    last_deployment_was_a_hotfix = False
    is_first_deployment = True
    nb_standard_deployments = 0  # Total number of deployments analyzed ; for the last one, we do not know
    nb_standard_deployments_without_hotfix = 0  # Initialize the count for deployments without hotfix

    for deployment in reversed(deployments):
        ref = deployment['ref']
        created_at = deployment['created_at']
        launched_at = deployment['updated_at']
        deployment_commit_message = deployment['deployable']['commit']['message']

        if deployment_commit_message.startswith("Merge branch 'hotfix"):
            print(black(f"Deployment ref={ref} launched_at={launched_at} {red('hotfix')}"))

            if is_first_deployment == True:
                nb_standard_deployments += 1 # A unknown deployment had a hotfix

            last_deployment_was_a_hotfix = True
        else:
            print(black(f"Deployment ref={ref} launched_at={launched_at}"))

            nb_standard_deployments += 1

            if not is_first_deployment == True and not last_deployment_was_a_hotfix:
                nb_standard_deployments_without_hotfix +=1

            if last_commit_date_of_previous_deployment:
                params = {
                    'since': last_commit_date_of_previous_deployment,
                    'until': launched_at,
                    'ref_name': branch,
                    'per_page': 100,
                }
                commits = get_commits(project_id, params)
                if args.debug: print("=> New Commits Since Previous Deployment:")
                if commits:
                    for commit in commits:
                        if not is_merge_commit(commit):
                            time_diff = get_time_delta(launched_at, commit['created_at'])
                            if args.debug: print(f"Commit: {commit['id']}, Commit Date: {commit['created_at']}, Commit Age Until Deploy: {format_time_difference(time_diff)}")
                            all_time_differences.append(time_diff)

            last_deployment_was_a_hotfix = False

            deployment_dates.add(launched_at.split('T')[0])  # Collect the date part, even for the first reference deployment

        last_commit_date_of_previous_deployment = created_at # there is nothing already deployed between created_at and effective_deployment_date
        is_first_deployment = False

    if len(deployments) > 0 and last_deployment_was_a_hotfix == False: # last deployment is considered clean if no hotfix after
        nb_standard_deployments_without_hotfix +=1

    print(green(f"=> {nb_standard_deployments - nb_standard_deployments_without_hotfix} deployments of features needed a later hotfix among {nb_standard_deployments} deployments of features for {project_id} on env"), magenta(env_name))

    if all_time_differences:
        median_time_difference = calculate_median_delta(all_time_differences)
        print(green(f"=> Median commit age before '{env_name}' deployment for {project_id}/{env_name}: {format_time_difference(median_time_difference)}"))

        return all_time_differences, deployment_dates, nb_standard_deployments_without_hotfix, nb_standard_deployments
    else:
        return None, set(), nb_standard_deployments_without_hotfix, nb_standard_deployments  # Return None if no deployments

# Function to check if a commit is a merge commit
def is_merge_commit(commit):
    parent_ids = commit.get('parent_ids', [])

    commit_message = commit.get('title', '')  # Get the commit message

    # Check if the commit message indicates a merge from a hotfix branch
    if commit_message.startswith("Merge branch 'hotfix"):
        if args.debug: print(f"This is a merge commit from a hotfix branch: {commit['id']}")

    if len(parent_ids) > 1: return True
    else: return False

# Function to calculate the average duration in seconds
def calculate_median_delta(time_deltas):
    delta_seconds = [time_delta.total_seconds() for time_delta in time_deltas]
    return timedelta(seconds=median(delta_seconds))

# Function to format a time difference as a human-readable string
def format_time_difference(time_diff):
    total_seconds = int(time_diff.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        return f"{minutes} minutes"
    else:
        return f"{seconds} seconds"

# Function to format a time difference as a human-readable string
def format_time_days(time_delta):
    return '{0:.2f}'.format(time_delta.total_seconds() / (24 * 60 * 60))

def get_average_pipeline_duration(project_id, updated_after):
    """
    gets the latest pipelines for the project
    ignore pipelines with status failed
    calculate the average duration
    """

    durations = []
    queued_duration: []
    coverage: []
    page = 1
    params = {
        'per_page': 100,
        'updated_after': updated_after,
        'status': "success",
        'source': "merge_request_event",
        'page': page
    }
    # get latest pipeline id list for given project_id
    while True:
        response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/pipelines', headers=headers, params=params)

        if response.status_code == 200:
            page_pipelines = response.json()
            # print(red(response.json()))
            if not page_pipelines:
                break  # No more pages, exit the loop
            for pipeline in page_pipelines:
                pipeline_response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/pipelines/{pipeline["id"]}', headers=headers)
                pipeline_detail = pipeline_response.json()
                # print(red(pipeline_response.json()))
                durations.append(timedelta(seconds=pipeline_detail["duration"]))
            page += 1
            params['page'] = page
        else:
            print(f"Error: {response.status_code} {response.reason}")
            break

    print(green(f"=> Pipeline duration '{durations}'"))
    if durations:
        median_duration = calculate_median_delta(durations)
        print(green(f"=> Median commit age before '{env_name}' deployment for {project_id}/{env_name}: {format_time_difference(median_duration)}"))

        return median_duration
    else:
        return None

# Function to get commits within a specified time range
def get_commits(project_id, params):
    if args.debug: print(f"Searching for commits with parameters {params}")
    commits = []

    # Initialize the page number to 1
    page = 1
    params['page'] = page

    while True:
        response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/repository/commits', headers=headers, params=params)

        if response.status_code == 200:
            page_commits = response.json()
            if not page_commits:
                break  # No more pages, exit the loop
            commits.extend(page_commits)
            page += 1
            params['page'] = page
        else:
            print(red(response.json()))
            break  # Handle errors or stop on non-200 response

    return commits

# Function to calculate time difference in seconds
def get_time_delta(end_time_str, start_time_str):
    end_time = datetime.fromisoformat(end_time_str)
    start_time = datetime.fromisoformat(start_time_str)
    time_delta = end_time - start_time
    return time_delta

# Function to retrieve project IDs for a group and its subgroups recursively
def get_project_ids_with_available_environments_for_group(group_id, full_path):
    nb_projects_found = 0
    project_ids_with_envs = []

    def get_projects_in_group(group_id, full_path, nb_projects_found):
        params = {
            'per_page': 100,
            'archived': False
        }
        response = requests.get(f'https://{args.gitlab_host}/api/v4/groups/{group_id}/subgroups', headers=headers, params=params)
        if response.status_code == 200:
            subgroups = response.json()
            for subgroup in subgroups:
                print(f"📁 found subgroup {cyan(subgroup['full_path'])} in {cyan(full_path)}")
                nb_projects_found = get_projects_in_group(subgroup['id'], subgroup['full_path'], nb_projects_found)
        else:
            print(red(response.json()))

        response = requests.get(f'https://{args.gitlab_host}/api/v4/groups/{group_id}/projects', headers=headers, params=params)
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                if full_path in project['path_with_namespace']:
                    nb_projects_found += 1
                    print(f" 🗒️ found project {cyan(project['path_with_namespace'])} in {cyan(full_path)}", end="")
                    environments_names = get_available_environments_names(project['id'])
                    if environments_names:
                        print(f", environments: {magenta(environments_names)}")
                        project_ids_with_envs.append(project['id'])
                    else:
                        print("")
                # weird bug: the API return projects not in the group O_o
        else:
            print(red(response.json()))

        return nb_projects_found

    nb_projects_found = get_projects_in_group(group_id, full_path, nb_projects_found)
    return nb_projects_found, project_ids_with_envs

def calculate_time_to_last_hotfix(project_id, deployments):
    ttlh_values = []
    last_hotfix_date = None

    for deployment in deployments:
        commit_message = deployment['deployable']['commit']['message']

        if commit_message.startswith("Merge branch 'hotfix"):
            last_hotfix_date = deployment['updated_at']
        else:
            if last_hotfix_date:
                time_delta = get_time_delta(last_hotfix_date, deployment['updated_at'])
                ttlh_values.append(time_delta)

    if ttlh_values:
        average_ttlh = calculate_median_delta(ttlh_values)
        print(green(f"=> Median Time To Last Hotfix for project {project_id}: {format_time_difference(average_ttlh)}"))
        return average_ttlh
    else:
        return None

def does_branch_exist(project_id, branch_name):
    params = {
        'per_page': 100,
    }
    response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/repository/branches', headers=headers, params=params)
    if response.status_code == 200:
        branches = response.json()
        return any(branch['name'] == branch_name for branch in branches)
    else:
        print(red(response.json()))
        return False

if __name__ == '__main__':

    updated_after = (datetime.now() - timedelta(days=args.days)).isoformat(timespec='milliseconds')
    print(yellow(f"Checking all deployments after {updated_after}"))
    nb_projects_found = 0

    if args.group_id:
        response = requests.get(f'https://{args.gitlab_host}/api/v4/groups/{args.group_id}', headers=headers)
        if response.status_code == 200:
            nb_projects_found, project_ids_with_env = get_project_ids_with_available_environments_for_group(args.group_id, response.json().get('full_path'))
        else:
            print(red("Group does not exist. Did you provide a project ID ?"))
            exit(1)
        if not project_ids_with_env:
            print("No projects with environments found in the group")
    elif args.project_ids:
        project_ids_with_env = [project_id.strip() for project_id in args.project_ids.split(',')]
        nb_projects_found = len(args.project_ids.split(','))
    else:
        print(red("You must provide either --group-id or --project-ids"))
        exit(1)

    projects_without_prod_env = set()
    projects_without_enough_deployment = set()
    projects_with_analyzed_deployments = set()
    all_projects_time_differences = []
    all_projects_ttlh = []
    all_deployments_dates = set()  # Collect deployment dates across all projects
    nb_total_deployments_without_hotfix = 0
    nb_total_deployments = 0

    for project_id in project_ids_with_env:
        environments_names = []
        has_prod_env = False

        response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}', headers=headers)

        if response.status_code != 200:
            print(red(f"Project {project_id} is not reachable (HTTP code {response.status_code})"))
            if args.debug: print(red(response.json()))
            continue

        project_info = response.json()
        project_name = project_info.get('path_with_namespace', 'Unknown Project')
        title = f' Processing project {project_name} (ID {project_id}) '
        print(f"{title:-^100}")
        environments_names = get_available_environments_names(project_id)
        print(f"Environments: {magenta(environments_names)}")

        branch = args.branch.split('|')[0]
        alternative_branch = args.branch.split('|')[1] or "none"

        # Check if the main branch exists
        if len(environments_names)>0 and not does_branch_exist(project_id, branch):
            if not does_branch_exist(project_id, alternative_branch):
                print(red(f"Branch(es) '{args.branch}' does not exist in project {project_name}"))
            else:
                branch = alternative_branch

        for env_name in environments_names:

            if not re.match(args.env, env_name):
                if args.debug: print(black(f"{env_name} does not match {args.env}"))
                continue
            else:
                has_prod_env = True

            deployments = get_last_successful_deployments(project_id, env_name)
            project_time_differences, project_deployment_dates, nb_project_deployments_without_hotfix, nb_project_deployments = process_deployments(project_id, env_name, deployments, branch)

            if project_time_differences is not None:
                all_projects_time_differences += project_time_differences
                projects_with_analyzed_deployments.add(project_name)
            else: # nb_deployments_without_hotfix < 2
                projects_without_enough_deployment.add(project_name)

            all_deployments_dates.update(project_deployment_dates)
            nb_total_deployments += nb_project_deployments
            nb_total_deployments_without_hotfix += nb_project_deployments_without_hotfix

            project_ttlh = calculate_time_to_last_hotfix(project_id, deployments)
            if project_ttlh is not None:
                all_projects_ttlh.append(project_ttlh)

        if has_prod_env == False:
            projects_without_prod_env.add(project_name)

        # print(f"average MR pipeline duration: {get_average_pipeline_duration(project_id, updated_after)}")

    print("")
    print(f"{nb_projects_found} total project(s) analyzed")
    print(f"{black(len(projects_without_prod_env))} project(s) have environments but not a '{args.env}' environment: {black(projects_without_prod_env)}")
    print(f"{blue(len(projects_without_enough_deployment))} project(s) have a '{args.env}' environment but only 0/1 deployment of features in the last {args.days} days: {blue(projects_without_enough_deployment)}")
    print(f"{green(len(projects_with_analyzed_deployments))} project(s) contributed to the metrics: {green(projects_with_analyzed_deployments)}")
    print(f"Checked deployments after {updated_after} (last {args.days} days)")

    if all_deployments_dates:
        num_days_with_deployments = len(all_deployments_dates)
        deployment_frequency_days = args.days / num_days_with_deployments
        print(f"Overall, there has been {green(num_days_with_deployments)} days with at least one non-hotfix deployment for the past {args.days} days")
        deployment_frequency_human_readable = format_time_difference(timedelta(days=deployment_frequency_days))
        print("")
        print(green(f"DORA Deployment Frequency:".ljust(30) + f"{deployment_frequency_days:.2f} days".ljust(15) + f"A deployment of features every {deployment_frequency_human_readable} on average (excluding hotfixes)"))

    if all_projects_time_differences:
        overall_median_time_difference = calculate_median_delta(all_projects_time_differences)
        print(green(f"DORA Lead Time for Changes:".ljust(30) + f"{format_time_days(overall_median_time_difference)} days".ljust(15) + f"The median feature commit age is {format_time_difference(overall_median_time_difference)} when deployed to production (excluding merge commits and hotfixes)"))

    if nb_total_deployments > 0:
        deployments_with_bug_ratio = 1 - ( nb_total_deployments_without_hotfix / nb_total_deployments)
        print(green(f"Deployments Needing Hotfix:".ljust(30) + f"{deployments_with_bug_ratio:.2%}".ljust(15) + f"{nb_total_deployments - nb_total_deployments_without_hotfix} deployments of features needed a later hotfix among {nb_total_deployments} deployments of features"))

    if all_projects_ttlh:
        overall_ttlh = calculate_median_delta(all_projects_ttlh)
        print(green(f"Time to Last Hotfix:".ljust(30) + f"{format_time_days(overall_ttlh)} days".ljust(15) + f"Last hotfix median delay after the associated deployment of features is {format_time_difference(overall_ttlh)}"))

    print("")
Wrapping up
In this article, we explored DevOps Research and Assessment (DORA) metrics, comparing various solutions and calculating key metrics like Lead Time, Deployment Frequency, Change Failure Rate, and Time to Restore Service. We contrasted GitLab's official calculations with our simpler alternatives, introduced a Python script for GitLab metric computation.

Whether using official solutions or our alternatives, the aim is clear: cultivate efficiency, reliability, and swift software delivery in the dynamic DevOps landscape. Check out the Python script for practical metric calculations! And feel free to provide feedback or suggestions in the comments below! 🚀

a humanoid fox from behind watching metrics dashboards, multiple computer monitors,manga style

Illustrations generated locally by Pinokio using Stable Cascade plugin

Further reading
Zenika 
🦊 GitLab CI: The Majestic Single Server Runner
Benoit COUETIL 💫 for Zenika ・ Jan 27
#gitlab #devops #pipeline #cicd
Zenika 
🦊 GitLab CI: Deploy a Majestic Single Server Runner on AWS
Benoit COUETIL 💫 for Zenika ・ Feb 17
#gitlab #devops #pipeline #tutorial
Zenika 
🦊 GitLab CI YAML Modifications: Tackling the Feedback Loop Problem
Benoit COUETIL 💫 for Zenika ・ Dec 18 '23
#gitlab #devops #pipeline #cicd
Zenika 
🦊 GitLab CI Optimization: 15+ Tips for Faster Pipelines
Benoit COUETIL 💫 for Zenika ・ Nov 6 '23
#gitlab #devops #pipeline #cicd
Zenika 
🦊 GitLab CI: 10+ Best Practices to Avoid Widespread Anti-patterns
Benoit COUETIL 💫 for Zenika ・ Sep 25 '23
#gitlab #devops #pipeline #cicd
Zenika 
🦊 GitLab Pages per Branch: The No-Compromise Hack to Serve Preview Pages
Benoit COUETIL 💫 for Zenika ・ Aug 1 '23
#gitlab #hack #devops #cicd
Zenika 
🦊 ChatGPT, If You Please, Make Me a GitLab Jobs Attributes Sorter
Benoit COUETIL 💫 for Zenika ・ Mar 30 '23
#chatgpt #gitlab #ai #python
Zenika 
🦊 GitLab Runners Topologies: Pros and Cons
Benoit COUETIL 💫 for Zenika ・ Feb 7 '23
#gitlab #devops #kubernetes #aws
This article was enhanced with the assistance of an AI language model to ensure clarity and accuracy in the content, as English is not my native language.

Top comments (0)
Subscribe
pic
Add to the discussion
Some comments may only be visible to logged-in visitors. Sign in to view all comments.

Code of Conduct • Report abuse
Read next
tungbq profile image
The DevOps Basics 🚀
Tung Leo - Mar 31

yayabobi profile image
The Developer's Guide to OWASP API Security
yayabobi - Apr 2

env0team profile image
A Complete Guide to Terraform Cloud Pricing
env0 Team - Apr 2

karadza profile image
Kubernetes Through the Developer's Perspective
Juraj - Mar 26


Zenika
Follow
More from Zenika
✨ Discovering GitLab Duo 🤖
#gitlab #ai #devops
☸️ Kubernetes: From your docker-compose file to a cluster with Kompose
#docker #kubernetes #devops #webdev
🦊 GitLab CI: Deploy a Majestic Single Server Runner on AWS
#gitlab #devops #pipeline #tutorial
"""
GitLab Dora Metrics Calculator for a project or all projects in a group

This script is designed to calculate key DORA (DevOps Research and Assessment) metrics for GitLab projects and groups.

The metrics and their computation include:
- DORA Deployment Frequency:
    - Measures how often code is deployed to production
    - Computed by counting the number of deployments of features (except hotfixes) to the production environment in a specified time period.
- DORA Lead Time for Changes:
    - Measures the time it takes for code changes to go from commit to deployment
    - Computed as the average time between feature commits (excluding merge commits and hotfixes) and their subsequent deployments.
- Deployments Needing Hotfix:
    - Measures the percentage of deployments that require additional hotfixes.
    - Computed by comparing the number of deployments that required a later hotfix to the total number of deployments of features.
- Time to Last Hotfix:
    - Measures how long it takes to hotfix the service after a deployment.
    - Computed as the average time between hotfix deployments and their associated feature deployments.

Prerequisites:
- pip install requests ansicolors
- An access to all the projects in the group
- Hotfixes are performed by branches whose name starts with 'hotfix', and merges are performed with a merge commit.
- Deployments are performed using the environment feature, and the production environments are distinguished by a common regex.

Usage:
python compute-dora-metrics.py --token <token> --days <nb_days> --group-id <group_id>
python compute-dora-metrics.py --token <token> --days <nb_days> --project-ids <project_id1>,<project_id2>,...

Arguments:
  --token          Your GitLab personal access token.
  --gitlab-host    Your GitLab host (default: gitlab.com).
  --group-id       The ID of the GitLab group to analyze.
  --project-ids    Comma-separated list of GitLab project IDs to analyze.
  --days           The duration of analysis in days (default: 90).
  --branch         The main branch (default: main).
  --env            The environment name for production deployments (default: 'prod*', in a subfolder or not).
  --debug          Whether to print more logs (default: false)

Author: Benoit COUETIL
"""

import requests
import argparse
import re
from datetime import datetime, timedelta
from colors import * # COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
from statistics import median

parser = argparse.ArgumentParser(description='Calculate DORA Metrics for a GitLab group and its projects.')
parser.add_argument('--token', required=True, help='Your GitLab personal access token')
parser.add_argument('--gitlab-host', default='gitlab.com', help='Your GitLab host')
parser.add_argument('--group-id', help='The ID of the GitLab group to analyze')
parser.add_argument('--project-ids', help='Comma-separated list of GitLab project IDs to analyze')
parser.add_argument('--branch', default='main|master', help='The main branch')
parser.add_argument('--env', default='(|.*\/)prod.*', help='The prod environment name pattern to match (not search) (default: (|.*\/)prod.*)')
parser.add_argument('--days', type=int, default=90, help='The duration of analysis in days (default 90)')
parser.add_argument("--debug", action=argparse.BooleanOptionalAction, help='Whether to print details of commits (default false)')
args = parser.parse_args()
headers = {'Private-Token': args.token}

def get_available_environments_names(project_id):

    environments_names = []

    params = {
        'per_page': 100,
        'states': 'available',
    }

    any_environment_response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/environments', headers=headers, params=params)
    if any_environment_response.status_code == 200:
        environments = any_environment_response.json()
        if environments:
            for environment in environments:
                environments_names.append(environment['name'])

    return environments_names

# Function to get the last 10 deployments of environment "prod" for a project
def get_last_successful_deployments(project_id, env_name):

    params = {
        'environment': env_name,
        'per_page': 100,
        'order_by': 'updated_at',
        'sort': 'desc',  # Sort in descending order (oldest first)
        'status': 'success',
        'updated_after': updated_after,
    }
    response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/deployments', headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        if args.debug: print(red(response.json()))
        return []

# Function to iterate over deployments and commits
def process_deployments(project_id, env_name, deployments, branch):
    if args.debug: print(f"Processing environment '{magenta(env_name)}'")
    last_commit_date_of_previous_deployment = None
    all_time_differences = []
    deployment_dates = set()  # Collect deployment dates for the project
    last_deployment_was_a_hotfix = False
    is_first_deployment = True
    nb_standard_deployments = 0  # Total number of deployments analyzed ; for the last one, we do not know
    nb_standard_deployments_without_hotfix = 0  # Initialize the count for deployments without hotfix

    for deployment in reversed(deployments):
        ref = deployment['ref']
        created_at = deployment['created_at']
        launched_at = deployment['updated_at']
        deployment_commit_message = deployment['deployable']['commit']['message']

        if deployment_commit_message.startswith("Merge branch 'hotfix"):
            print(black(f"Deployment ref={ref} launched_at={launched_at} {red('hotfix')}"))

            if is_first_deployment == True:
                nb_standard_deployments += 1 # A unknown deployment had a hotfix

            last_deployment_was_a_hotfix = True
        else:
            print(black(f"Deployment ref={ref} launched_at={launched_at}"))

            nb_standard_deployments += 1

            if not is_first_deployment == True and not last_deployment_was_a_hotfix:
                nb_standard_deployments_without_hotfix +=1

            if last_commit_date_of_previous_deployment:
                params = {
                    'since': last_commit_date_of_previous_deployment,
                    'until': launched_at,
                    'ref_name': branch,
                    'per_page': 100,
                }
                commits = get_commits(project_id, params)
                if args.debug: print("=> New Commits Since Previous Deployment:")
                if commits:
                    for commit in commits:
                        if not is_merge_commit(commit):
                            time_diff = get_time_delta(launched_at, commit['created_at'])
                            if args.debug: print(f"Commit: {commit['id']}, Commit Date: {commit['created_at']}, Commit Age Until Deploy: {format_time_difference(time_diff)}")
                            all_time_differences.append(time_diff)

            last_deployment_was_a_hotfix = False

            deployment_dates.add(launched_at.split('T')[0])  # Collect the date part, even for the first reference deployment

        last_commit_date_of_previous_deployment = created_at # there is nothing already deployed between created_at and effective_deployment_date
        is_first_deployment = False

    if len(deployments) > 0 and last_deployment_was_a_hotfix == False: # last deployment is considered clean if no hotfix after
        nb_standard_deployments_without_hotfix +=1

    print(green(f"=> {nb_standard_deployments - nb_standard_deployments_without_hotfix} deployments of features needed a later hotfix among {nb_standard_deployments} deployments of features for {project_id} on env"), magenta(env_name))

    if all_time_differences:
        median_time_difference = calculate_median_delta(all_time_differences)
        print(green(f"=> Median commit age before '{env_name}' deployment for {project_id}/{env_name}: {format_time_difference(median_time_difference)}"))

        return all_time_differences, deployment_dates, nb_standard_deployments_without_hotfix, nb_standard_deployments
    else:
        return None, set(), nb_standard_deployments_without_hotfix, nb_standard_deployments  # Return None if no deployments

# Function to check if a commit is a merge commit
def is_merge_commit(commit):
    parent_ids = commit.get('parent_ids', [])

    commit_message = commit.get('title', '')  # Get the commit message

    # Check if the commit message indicates a merge from a hotfix branch
    if commit_message.startswith("Merge branch 'hotfix"):
        if args.debug: print(f"This is a merge commit from a hotfix branch: {commit['id']}")

    if len(parent_ids) > 1: return True
    else: return False

# Function to calculate the average duration in seconds
def calculate_median_delta(time_deltas):
    delta_seconds = [time_delta.total_seconds() for time_delta in time_deltas]
    return timedelta(seconds=median(delta_seconds))

# Function to format a time difference as a human-readable string
def format_time_difference(time_diff):
    total_seconds = int(time_diff.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days > 0:
        return f"{days} days, {hours} hours, {minutes} minutes"
    elif hours > 0:
        return f"{hours} hours, {minutes} minutes"
    elif minutes > 0:
        return f"{minutes} minutes"
    else:
        return f"{seconds} seconds"

# Function to format a time difference as a human-readable string
def format_time_days(time_delta):
    return '{0:.2f}'.format(time_delta.total_seconds() / (24 * 60 * 60))

def get_average_pipeline_duration(project_id, updated_after):
    """
    gets the latest pipelines for the project
    ignore pipelines with status failed
    calculate the average duration
    """

    durations = []
    queued_duration: []
    coverage: []
    page = 1
    params = {
        'per_page': 100,
        'updated_after': updated_after,
        'status': "success",
        'source': "merge_request_event",
        'page': page
    }
    # get latest pipeline id list for given project_id
    while True:
        response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/pipelines', headers=headers, params=params)

        if response.status_code == 200:
            page_pipelines = response.json()
            # print(red(response.json()))
            if not page_pipelines:
                break  # No more pages, exit the loop
            for pipeline in page_pipelines:
                pipeline_response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/pipelines/{pipeline["id"]}', headers=headers)
                pipeline_detail = pipeline_response.json()
                # print(red(pipeline_response.json()))
                durations.append(timedelta(seconds=pipeline_detail["duration"]))
            page += 1
            params['page'] = page
        else:
            print(f"Error: {response.status_code} {response.reason}")
            break

    print(green(f"=> Pipeline duration '{durations}'"))
    if durations:
        median_duration = calculate_median_delta(durations)
        print(green(f"=> Median commit age before '{env_name}' deployment for {project_id}/{env_name}: {format_time_difference(median_duration)}"))

        return median_duration
    else:
        return None

# Function to get commits within a specified time range
def get_commits(project_id, params):
    if args.debug: print(f"Searching for commits with parameters {params}")
    commits = []

    # Initialize the page number to 1
    page = 1
    params['page'] = page

    while True:
        response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/repository/commits', headers=headers, params=params)

        if response.status_code == 200:
            page_commits = response.json()
            if not page_commits:
                break  # No more pages, exit the loop
            commits.extend(page_commits)
            page += 1
            params['page'] = page
        else:
            print(red(response.json()))
            break  # Handle errors or stop on non-200 response

    return commits

# Function to calculate time difference in seconds
def get_time_delta(end_time_str, start_time_str):
    end_time = datetime.fromisoformat(end_time_str)
    start_time = datetime.fromisoformat(start_time_str)
    time_delta = end_time - start_time
    return time_delta

# Function to retrieve project IDs for a group and its subgroups recursively
def get_project_ids_with_available_environments_for_group(group_id, full_path):
    nb_projects_found = 0
    project_ids_with_envs = []

    def get_projects_in_group(group_id, full_path, nb_projects_found):
        params = {
            'per_page': 100,
            'archived': False
        }
        response = requests.get(f'https://{args.gitlab_host}/api/v4/groups/{group_id}/subgroups', headers=headers, params=params)
        if response.status_code == 200:
            subgroups = response.json()
            for subgroup in subgroups:
                print(f"📁 found subgroup {cyan(subgroup['full_path'])} in {cyan(full_path)}")
                nb_projects_found = get_projects_in_group(subgroup['id'], subgroup['full_path'], nb_projects_found)
        else:
            print(red(response.json()))

        response = requests.get(f'https://{args.gitlab_host}/api/v4/groups/{group_id}/projects', headers=headers, params=params)
        if response.status_code == 200:
            projects = response.json()
            for project in projects:
                if full_path in project['path_with_namespace']:
                    nb_projects_found += 1
                    print(f" 🗒️ found project {cyan(project['path_with_namespace'])} in {cyan(full_path)}", end="")
                    environments_names = get_available_environments_names(project['id'])
                    if environments_names:
                        print(f", environments: {magenta(environments_names)}")
                        project_ids_with_envs.append(project['id'])
                    else:
                        print("")
                # weird bug: the API return projects not in the group O_o
        else:
            print(red(response.json()))

        return nb_projects_found

    nb_projects_found = get_projects_in_group(group_id, full_path, nb_projects_found)
    return nb_projects_found, project_ids_with_envs

def calculate_time_to_last_hotfix(project_id, deployments):
    ttlh_values = []
    last_hotfix_date = None

    for deployment in deployments:
        commit_message = deployment['deployable']['commit']['message']

        if commit_message.startswith("Merge branch 'hotfix"):
            last_hotfix_date = deployment['updated_at']
        else:
            if last_hotfix_date:
                time_delta = get_time_delta(last_hotfix_date, deployment['updated_at'])
                ttlh_values.append(time_delta)

    if ttlh_values:
        average_ttlh = calculate_median_delta(ttlh_values)
        print(green(f"=> Median Time To Last Hotfix for project {project_id}: {format_time_difference(average_ttlh)}"))
        return average_ttlh
    else:
        return None

def does_branch_exist(project_id, branch_name):
    params = {
        'per_page': 100,
    }
    response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}/repository/branches', headers=headers, params=params)
    if response.status_code == 200:
        branches = response.json()
        return any(branch['name'] == branch_name for branch in branches)
    else:
        print(red(response.json()))
        return False

if __name__ == '__main__':

    updated_after = (datetime.now() - timedelta(days=args.days)).isoformat(timespec='milliseconds')
    print(yellow(f"Checking all deployments after {updated_after}"))
    nb_projects_found = 0

    if args.group_id:
        response = requests.get(f'https://{args.gitlab_host}/api/v4/groups/{args.group_id}', headers=headers)
        if response.status_code == 200:
            nb_projects_found, project_ids_with_env = get_project_ids_with_available_environments_for_group(args.group_id, response.json().get('full_path'))
        else:
            print(red("Group does not exist. Did you provide a project ID ?"))
            exit(1)
        if not project_ids_with_env:
            print("No projects with environments found in the group")
    elif args.project_ids:
        project_ids_with_env = [project_id.strip() for project_id in args.project_ids.split(',')]
        nb_projects_found = len(args.project_ids.split(','))
    else:
        print(red("You must provide either --group-id or --project-ids"))
        exit(1)

    projects_without_prod_env = set()
    projects_without_enough_deployment = set()
    projects_with_analyzed_deployments = set()
    all_projects_time_differences = []
    all_projects_ttlh = []
    all_deployments_dates = set()  # Collect deployment dates across all projects
    nb_total_deployments_without_hotfix = 0
    nb_total_deployments = 0

    for project_id in project_ids_with_env:
        environments_names = []
        has_prod_env = False

        response = requests.get(f'https://{args.gitlab_host}/api/v4/projects/{project_id}', headers=headers)

        if response.status_code != 200:
            print(red(f"Project {project_id} is not reachable (HTTP code {response.status_code})"))
            if args.debug: print(red(response.json()))
            continue

        project_info = response.json()
        project_name = project_info.get('path_with_namespace', 'Unknown Project')
        title = f' Processing project {project_name} (ID {project_id}) '
        print(f"{title:-^100}")
        environments_names = get_available_environments_names(project_id)
        print(f"Environments: {magenta(environments_names)}")

        branch = args.branch.split('|')[0]
        alternative_branch = args.branch.split('|')[1] or "none"

        # Check if the main branch exists
        if len(environments_names)>0 and not does_branch_exist(project_id, branch):
            if not does_branch_exist(project_id, alternative_branch):
                print(red(f"Branch(es) '{args.branch}' does not exist in project {project_name}"))
            else:
                branch = alternative_branch

        for env_name in environments_names:

            if not re.match(args.env, env_name):
                if args.debug: print(black(f"{env_name} does not match {args.env}"))
                continue
            else:
                has_prod_env = True

            deployments = get_last_successful_deployments(project_id, env_name)
            project_time_differences, project_deployment_dates, nb_project_deployments_without_hotfix, nb_project_deployments = process_deployments(project_id, env_name, deployments, branch)

            if project_time_differences is not None:
                all_projects_time_differences += project_time_differences
                projects_with_analyzed_deployments.add(project_name)
            else: # nb_deployments_without_hotfix < 2
                projects_without_enough_deployment.add(project_name)

            all_deployments_dates.update(project_deployment_dates)
            nb_total_deployments += nb_project_deployments
            nb_total_deployments_without_hotfix += nb_project_deployments_without_hotfix

            project_ttlh = calculate_time_to_last_hotfix(project_id, deployments)
            if project_ttlh is not None:
                all_projects_ttlh.append(project_ttlh)

        if has_prod_env == False:
            projects_without_prod_env.add(project_name)

        # print(f"average MR pipeline duration: {get_average_pipeline_duration(project_id, updated_after)}")

    print("")
    print(f"{nb_projects_found} total project(s) analyzed")
    print(f"{black(len(projects_without_prod_env))} project(s) have environments but not a '{args.env}' environment: {black(projects_without_prod_env)}")
    print(f"{blue(len(projects_without_enough_deployment))} project(s) have a '{args.env}' environment but only 0/1 deployment of features in the last {args.days} days: {blue(projects_without_enough_deployment)}")
    print(f"{green(len(projects_with_analyzed_deployments))} project(s) contributed to the metrics: {green(projects_with_analyzed_deployments)}")
    print(f"Checked deployments after {updated_after} (last {args.days} days)")

    if all_deployments_dates:
        num_days_with_deployments = len(all_deployments_dates)
        deployment_frequency_days = args.days / num_days_with_deployments
        print(f"Overall, there has been {green(num_days_with_deployments)} days with at least one non-hotfix deployment for the past {args.days} days")
        deployment_frequency_human_readable = format_time_difference(timedelta(days=deployment_frequency_days))
        print("")
        print(green(f"DORA Deployment Frequency:".ljust(30) + f"{deployment_frequency_days:.2f} days".ljust(15) + f"A deployment of features every {deployment_frequency_human_readable} on average (excluding hotfixes)"))

    if all_projects_time_differences:
        overall_median_time_difference = calculate_median_delta(all_projects_time_differences)
        print(green(f"DORA Lead Time for Changes:".ljust(30) + f"{format_time_days(overall_median_time_difference)} days".ljust(15) + f"The median feature commit age is {format_time_difference(overall_median_time_difference)} when deployed to production (excluding merge commits and hotfixes)"))

    if nb_total_deployments > 0:
        deployments_with_bug_ratio = 1 - ( nb_total_deployments_without_hotfix / nb_total_deployments)
        print(green(f"Deployments Needing Hotfix:".ljust(30) + f"{deployments_with_bug_ratio:.2%}".ljust(15) + f"{nb_total_deployments - nb_total_deployments_without_hotfix} deployments of features needed a later hotfix among {nb_total_deployments} deployments of features"))

    if all_projects_ttlh:
        overall_ttlh = calculate_median_delta(all_projects_ttlh)
        print(green(f"Time to Last Hotfix:".ljust(30) + f"{format_time_days(overall_ttlh)} days".ljust(15) + f"Last hotfix median delay after the associated deployment of features is {format_time_difference(overall_ttlh)}"))

    print("")