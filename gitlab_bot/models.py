from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    username: str
    avatar_url: str
    email: str


class Project(BaseModel):
    id: int
    name: str
    description: Any
    web_url: str
    avatar_url: Any
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: str
    homepage: str
    url: str
    ssh_url: str
    http_url: str


class ObjectAttributes(BaseModel):
    author_id: int
    closed_at: Any
    confidential: bool
    created_at: str
    description: str
    discussion_locked: Any
    due_date: Any
    id: int
    iid: int
    last_edited_at: Any
    last_edited_by_id: Any
    milestone_id: Any
    moved_to_id: Any
    duplicated_to_id: Any
    project_id: int
    relative_position: Any
    state_id: int
    time_estimate: int
    title: str
    updated_at: str
    updated_by_id: Any
    weight: Any
    url: str
    total_time_spent: int
    time_change: int
    human_total_time_spent: Any
    human_time_change: Any
    human_time_estimate: Any
    assignee_ids: List
    assignee_id: Any
    labels: List
    state: str
    severity: str
    action: Optional[str]


class AuthorId(BaseModel):
    previous: Any
    current: int


class CreatedAt(BaseModel):
    previous: Any
    current: str


class Description(BaseModel):
    previous: Any
    current: str


class Id(BaseModel):
    previous: Any
    current: int


class Iid(BaseModel):
    previous: Any
    current: int


class ProjectId(BaseModel):
    previous: Any
    current: int


class TimeEstimate(BaseModel):
    previous: Any
    current: int


class Title(BaseModel):
    previous: Any
    current: str


class UpdatedAt(BaseModel):
    previous: Any
    current: str


class Changes(BaseModel):
    author_id: Optional[AuthorId]
    created_at: Optional[CreatedAt]
    description: Optional[Description]
    id: Optional[Id]
    iid: Optional[Iid]
    project_id: Optional[ProjectId]
    time_estimate: Optional[TimeEstimate]
    title: Optional[Title]
    updated_at: Optional[UpdatedAt]


class Repository(BaseModel):
    name: str
    url: str
    description: Any
    homepage: str


class WebhookIssue(BaseModel):
    object_kind: str
    event_type: str
    user: User
    project: Project
    object_attributes: ObjectAttributes
    labels: List
    changes: Optional[Changes]
    repository: Repository

if __name__ == '__main__':
    import json
    t = json.loads('''
    {
  "object_kind": "issue",
  "event_type": "issue",
  "user": {
    "id": 1788222,
    "name": "Dmitry Chermnykh",
    "username": "chermnyx",
    "avatar_url": "https://gitlab.com/uploads/-/system/user/avatar/1788222/avatar.png",
    "email": "[REDACTED]"
  },
  "project": {
    "id": 43444614,
    "name": "vdo_test",
    "description": null,
    "web_url": "https://gitlab.com/chermnyx/vdo_test",
    "avatar_url": null,
    "git_ssh_url": "git@gitlab.com:chermnyx/vdo_test.git",
    "git_http_url": "https://gitlab.com/chermnyx/vdo_test.git",
    "namespace": "Dmitry Chermnykh",
    "visibility_level": 0,
    "path_with_namespace": "chermnyx/vdo_test",
    "default_branch": "main",
    "ci_config_path": "",
    "homepage": "https://gitlab.com/chermnyx/vdo_test",
    "url": "git@gitlab.com:chermnyx/vdo_test.git",
    "ssh_url": "git@gitlab.com:chermnyx/vdo_test.git",
    "http_url": "https://gitlab.com/chermnyx/vdo_test.git"
  },
  "object_attributes": {
    "author_id": 1788222,
    "closed_at": null,
    "confidential": false,
    "created_at": "2023-02-12 13:18:03 UTC",
    "description": "Confirm security bug in app/main.py",
    "discussion_locked": null,
    "due_date": null,
    "id": 123545137,
    "iid": 1,
    "last_edited_at": null,
    "last_edited_by_id": null,
    "milestone_id": null,
    "moved_to_id": null,
    "duplicated_to_id": null,
    "project_id": 43444614,
    "relative_position": null,
    "state_id": 1,
    "time_estimate": 0,
    "title": "Test",
    "updated_at": "2023-02-12 13:18:03 UTC",
    "updated_by_id": null,
    "weight": null,
    "url": "https://gitlab.com/chermnyx/vdo_test/-/issues/1",
    "total_time_spent": 0,
    "time_change": 0,
    "human_total_time_spent": null,
    "human_time_change": null,
    "human_time_estimate": null,
    "assignee_ids": [

    ],
    "assignee_id": null,
    "labels": [

    ],
    "state": "opened",
    "severity": "unknown",
    "action": "open"
  },
  "labels": [

  ],
  "changes": {
    "author_id": {
      "previous": null,
      "current": 1788222
    },
    "created_at": {
      "previous": null,
      "current": "2023-02-12 13:18:03 UTC"
    },
    "description": {
      "previous": null,
      "current": "Confirm security bug in app/main.py"
    },
    "id": {
      "previous": null,
      "current": 123545137
    },
    "iid": {
      "previous": null,
      "current": 1
    },
    "project_id": {
      "previous": null,
      "current": 43444614
    },
    "time_estimate": {
      "previous": null,
      "current": 0
    },
    "title": {
      "previous": null,
      "current": "Test"
    },
    "updated_at": {
      "previous": null,
      "current": "2023-02-12 13:18:03 UTC"
    }
  },
  "repository": {
    "name": "vdo_test",
    "url": "git@gitlab.com:chermnyx/vdo_test.git",
    "description": null,
    "homepage": "https://gitlab.com/chermnyx/vdo_test"
  }
}
    ''')

    t = WebhookIssue.parse_obj(t)
    pass
