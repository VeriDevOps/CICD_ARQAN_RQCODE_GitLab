from typing import Optional

from gitlab.v4.objects import Project
from fastapi import FastAPI, Header, HTTPException

from . import cfg
from .models import WebhookIssue

app = FastAPI()

async def get_api_response(text: str):
    # FIXME: replace the placeholder with the proper api query
    return "Test response ඞ"

async def process_text(text: str, issue_id: int, project: Project = cfg.project):
    issue = project.issues.get(issue_id)

    response = await get_api_response(text)
    # TODO: check if the issue is supposed to be a security issue
    issue.labels.append('security')
    issue.save()

    issue.discussions.create({'body': response})

    return 'OK'

@app.post("/webhook/{webhook_prefix}")
async def create_item(webhook_prefix: str, item: WebhookIssue, x_gitlab_token: Optional[str] = Header(default=None)):
    if webhook_prefix != cfg.WEBHOOK_PREFIX:
        raise HTTPException(status_code=404)
    if x_gitlab_token != cfg.WEBHOOK_TOKEN:
        raise HTTPException(status_code=403)

    return {'text': await process_text(item.object_attributes.description, item.object_attributes.iid)}
