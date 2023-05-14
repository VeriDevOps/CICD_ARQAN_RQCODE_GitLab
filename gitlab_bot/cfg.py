import os
import git
import gitlab

WEBHOOK_PREFIX = os.environ['WEBHOOK_PREFIX']
WEBHOOK_TOKEN = os.environ['WEBHOOK_TOKEN']
GITLAB_INSTANCE = os.environ['GITLAB_INSTANCE']
GITLAB_REPO = os.environ['GITLAB_REPO']
GITLAB_TOKEN = os.environ['GITLAB_TOKEN']
ARQAN_SERVICES_API = os.environ['ARQAN_SERVICES_API']
ARQAN_PLATFORM = os.environ['ARQAN_PLATFORM']
ARQAN_USERNAME = os.environ.get('ARQAN_USERNAME')
ARQAN_PASSWORD = os.environ.get('ARQAN_PASSWORD')
PRODUCTION = bool(os.environ.get('PRODUCTION', False))

RQCODE_REPO = os.environ.get('RQCODE_REPO', 'https://github.com/VeriDevOps/RQCODE')
RQCODE_REPO_PATH= os.environ.get('RQCODE_REPO_PATH', '/var/tmp/rqcode')

gl = gitlab.Gitlab(url=GITLAB_INSTANCE, private_token=GITLAB_TOKEN)

try:
    rqcode_repo = git.Repo.clone_from(RQCODE_REPO, RQCODE_REPO_PATH)
except git.exc.GitCommandError:
    rqcode_repo = git.Repo(RQCODE_REPO_PATH)

if not PRODUCTION:
    gl.enable_debug()

project = gl.projects.get(GITLAB_REPO)
