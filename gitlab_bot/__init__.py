from pathlib import Path
from typing import Optional

import jinja2
import requests
from fastapi import FastAPI, Header, HTTPException
from gitlab.v4.objects import Project

from . import cfg
from .models import WebhookIssue

app = FastAPI()

env = jinja2.Environment(loader=jinja2.FileSystemLoader(str((Path(__file__).parent / 'templates').resolve())))

def get_api_response(text: str):
    result = requests.get(f'{cfg.ARQAN_SERVICES_API}/stigs', params={'text': text, 'platform': 'ubuntu', 't_type': 0})
    j = result.json()
    return j

def process_text(text: str, issue_id: int, project: Project = cfg.project):
    issue = project.issues.get(issue_id)

    response = get_api_response(text)
    if len(response):
        issue.labels.append('security')
        issue.save()

        stig_comment = env.get_template('stigs.md.j2').render(stigs=response)

        issue.discussions.create({'body': stig_comment})

    return 'OK'

@app.post("/webhook/{webhook_prefix}")
async def create_item(webhook_prefix: str, item: WebhookIssue, x_gitlab_token: Optional[str] = Header(default=None)):
    if webhook_prefix != cfg.WEBHOOK_PREFIX:
        raise HTTPException(status_code=404)
    if x_gitlab_token != cfg.WEBHOOK_TOKEN:
        raise HTTPException(status_code=403)

    return {'text': process_text(item.object_attributes.description, item.object_attributes.iid)}
