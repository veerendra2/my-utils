import os
import subprocess
import requests
import logging
from git import Repo
from time import sleep

# Set up logging to log to both console and file
log_file = 'migration.log'
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Fetch configuration from environment variables
GITEA_URL = os.getenv("GITEA_URL", "https://your-gitea-instance.com")
GITEA_API_TOKEN = os.getenv("GITEA_API_TOKEN", "your-gitea-api-token")
GITEA_USERNAME = os.getenv("GITEA_USERNAME", "your-username")
ORG_NAME = os.getenv("ORG_NAME", "your-organization")
LOCAL_REPOS_DIR = os.getenv("LOCAL_REPOS_DIR", "/path/to/your/local/repos")
WAIT_SECONDS = 120
DEFAULT_BRANCH = "main"

def create_gitea_repo(repo_name):
    """Create a new repository in the given Gitea organization using Gitea API."""
    url = f"{GITEA_URL}/api/v1/orgs/{ORG_NAME}/repos"
    headers = {
        "Authorization": f"token {GITEA_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": repo_name,
        "private": False,  # Set to True for private repos
        "default_branch": DEFAULT_BRANCH,
        "has_wiki": False,  # Disable the wiki
        "has_issues": False,  # Disable issues
        "has_actions": False,  # Disable actions
    }

    def disable_actions():
        repo_endpoint = f"{GITEA_URL}/api/v1/repos/{ORG_NAME}/{repo_name}"
        repo_settings_payload = {
            "has_actions": False  # Disable Actions
        }
        res = requests.patch(repo_endpoint, json=repo_settings_payload, headers=headers)
        if res.status_code == 200:
            logger.info( f"Actions successfully disabled for repository '{ORG_NAME}/{repo_name}'.")
        else:
            logger.wanring(f"Failed to disable Actions: {res.status_code}, {res.text}")

    # Check if repository already exists by first fetching the list of repos in the org
    check_url = f"{GITEA_URL}/api/v1/orgs/{ORG_NAME}/repos"
    response = requests.get(check_url, headers=headers)

    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            if repo["name"] == repo_name:
                logger.info(f"Repository {repo_name} already exists in Gitea. Skipping creation.")
                disable_actions()
                return repo["clone_url"]

    # Create the repository if it doesn't exist
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        logger.info(f"Successfully created repository: {repo_name}")
        disable_actions()
        return response.json()["clone_url"]
    else:
        logger.error(f"Failed to create repository {repo_name}: {response.text}")
        return None


def set_default_branch(repo, branch_name):
    """Switch to the default branch (main) if necessary and push it."""
    try:
        # Check if the default branch exists
        if branch_name in repo.branches:
            logger.info(f"Branch '{branch_name}' already exists. Switching to it.")
            repo.git.checkout(branch_name)
        else:
            logger.info(f"Default branch is not '{branch_name}', creating and switching to '{branch_name}'")
            repo.git.checkout("-b", branch_name)
            repo.git.push("-u", "origin", branch_name)

        # Set the default branch on Gitea using API
        repo_name = repo.remotes.origin.url.split("/")[-1].replace(".git", "")
        url = f"{GITEA_URL}/api/v1/repos/{ORG_NAME}/{repo_name}/branches/{branch_name}"
        headers = {
            "Authorization": f"token {GITEA_API_TOKEN}",
        }
        data = {"default": True}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            logger.info(f"Successfully set default branch to '{branch_name}'")
        else:
            logger.warning(f"Failed to set default branch: {response.text}")

    except Exception as e:
        logger.error(f"Failed to set default branch or switch to it: {str(e)}")

def push_to_gitea(repo_path, gitea_url):
    """Push the local git repository to Gitea."""
    try:
        repo = Repo(repo_path)

        # Check if remote 'origin' exists
        if 'origin' in repo.remotes:
            logger.info(f"Remote 'origin' already exists. Updating remote URL to {gitea_url}")
            origin = repo.remotes.origin
            origin.set_url(gitea_url)
        else:
            logger.info(f"Adding remote 'origin' with URL: {gitea_url}")
            origin = repo.create_remote("origin", gitea_url)

        # Set default branch if not already set to main
        set_default_branch(repo, DEFAULT_BRANCH)

        # Push the repository to Gitea (automated login using personal access token)
        repo.git.push("--set-upstream", "origin", DEFAULT_BRANCH)
        logger.info(f"Successfully pushed repository {repo_path} to Gitea.")

        logger.info(f"Sleep for {WAIT_SECONDS} seconds...")
        sleep(WAIT_SECONDS)

    except Exception as e:
        logger.error(f"Failed to push repository {repo_path} to Gitea: {str(e)}")

def is_git_repo(directory):
    """Check if the directory is a Git repository."""
    return os.path.isdir(os.path.join(directory, ".git"))

def process_local_repos(base_dir):
    """Traverse all directories and process git repos."""
    for root, dirs, files in os.walk(base_dir):
        if is_git_repo(root):
            logger.info(f"Found git repository: {root}")
            repo_name = os.path.basename(root)
            gitea_repo_url = create_gitea_repo(repo_name)

            if gitea_repo_url:
                logger.info(f"Pushing repository {repo_name} to Gitea...")
                # Add the Gitea authentication token directly into the URL
                auth_gitea_url = f"https://{GITEA_USERNAME}:{GITEA_API_TOKEN}@{gitea_repo_url.replace('https://', '')}"
                push_to_gitea(root, auth_gitea_url)

if __name__ == "__main__":
    process_local_repos(LOCAL_REPOS_DIR)
