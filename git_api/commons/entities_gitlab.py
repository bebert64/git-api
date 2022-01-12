from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from git_api.commons.types import GitlabId


@dataclass
class GitEntity:
    gitlab_id: GitlabId


@dataclass
class Member(GitEntity):
    username: str
    name: str
    role: str


@dataclass
class Group(GitEntity):
    name: str
    web_url: str
    description: str
    project_creation_level: str
    parent: Optional[Group]


@dataclass
class Project(GitEntity):
    name: str
    description: str
    web_url: str
    default_branch: str
    topics: str
    group: Optional[Group] = None


@dataclass
class Branch(GitEntity):
    name: str
    project: Project
    is_default: bool
    is_protected: bool
    developers_can_push: bool
    developers_can_merge: bool
    can_push: bool


@dataclass
class Commit(GitEntity):
    title: str
    author_name: str
    author_email: str
    committed_date: date
    message: str
    web_url: str
    branch: Branch
    member: Member


@dataclass
class Tag(GitEntity):
    commit: Commit
    name: str
    message: str