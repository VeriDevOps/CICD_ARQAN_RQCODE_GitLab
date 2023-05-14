from pathlib import Path
from typing import Optional

import jinja2
import requests
from fastapi import FastAPI, Header, HTTPException
from gitlab.v4.objects import Project, ProjectIssue

from . import cfg
from .models import WebhookIssue

app = FastAPI()

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str((Path(__file__).parent / "templates").resolve()))
)


def get_api_response(text: str):
    result = requests.get(
        f"{cfg.ARQAN_SERVICES_API}/stigs",
        params={"text": text, "platform": cfg.ARQAN_PLATFORM, "t_type": 0},
    )
    j = result.json()
    return j


def process_text(text: str, issue_id: int, project: Project = cfg.project):
    issue = project.issues.get(issue_id)

    response = get_api_response(text)
    if len(response):
        issue.labels.append("security")
        issue.save()

        stig_comment = env.get_template("stigs.md.j2").render(stigs=response)

        stig_ids = [ref[1].split('/')[-1].replace('-', '_') for stig_refs in response.values() for ref in stig_refs ]

        issue.discussions.create({"body": stig_comment})
        process_rqcode(stig_ids, issue)

        return stig_comment

    return None


def process_rqcode(stig_ids: list[str], issue: ProjectIssue):
    cfg.rqcode_repo.remotes.origin.pull()
    workdir = Path(cfg.rqcode_repo.working_tree_dir)
    rqs = []

    for stig_id in stig_ids:
        rqs.extend(workdir.glob(f"**/{stig_id}"))
        rqs.extend(workdir.glob(f"**/{stig_id}.java"))

    rqs = [str(rq.relative_to(workdir)) for rq in rqs]

    stig_comment = env.get_template("rqs.md.j2").render(
        rqs=rqs, rqcode_repo=cfg.RQCODE_REPO
    )
    issue.discussions.create({"body": stig_comment})


@app.post("/webhook/{webhook_prefix}")
async def create_item(
    webhook_prefix: str,
    item: WebhookIssue,
    x_gitlab_token: Optional[str] = Header(default=None),
):
    if webhook_prefix != cfg.WEBHOOK_PREFIX:
        raise HTTPException(status_code=404)
    if x_gitlab_token != cfg.WEBHOOK_TOKEN:
        raise HTTPException(status_code=403)

    return {
        "text": process_text(
            item.object_attributes.title
            + "\n"
            + (item.object_attributes.description or ""),
            item.object_attributes.iid,
        )
    }
