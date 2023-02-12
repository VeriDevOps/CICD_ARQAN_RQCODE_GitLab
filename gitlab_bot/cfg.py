import os
import gitlab

WEBHOOK_PREFIX = os.environ['WEBHOOK_PREFIX']
WEBHOOK_TOKEN = os.environ['WEBHOOK_TOKEN']
GITLAB_INSTANCE = os.environ['GITLAB_INSTANCE']
GITLAB_REPO = os.environ['GITLAB_REPO']
GITLAB_TOKEN = os.environ['GITLAB_TOKEN']
PRODUCTION = bool(os.environ.get('PRODUCTION', False))

gl = gitlab.Gitlab(url=GITLAB_INSTANCE, private_token=GITLAB_TOKEN)

if not PRODUCTION:
    gl.enable_debug()

project = gl.projects.get(GITLAB_REPO)
