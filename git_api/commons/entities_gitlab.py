from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from git_api.commons.types import GitlabId


@dataclass
class EntityGitlab:
    gitlab_id: GitlabId


@dataclass
class Member(EntityGitlab):
    username: str
    name: str
    role: str


@dataclass
class Group(EntityGitlab):
    name: str
    web_url: str
    description: str
    project_creation_level: str
    parent: Optional[Group]


@dataclass
class Project(EntityGitlab):
    name: str
    description: str
    web_url: str
    default_branch: str
    topics: str
    group: Optional[Group] = None


@dataclass
class Branch(EntityGitlab):
    name: str
    project: Optional[Project]
    is_default: bool
    is_protected: bool
    developers_can_push: bool
    developers_can_merge: bool
    can_push: bool


@dataclass
class Commit(EntityGitlab):  # pylint: disable=too-many-instance-attributes
    title: str = ""
    author_name: str = ""
    author_email: str = ""
    committed_date: date = date.today()
    message: str = ""
    web_url: str = ""
    branch: Optional[Branch] = None
    member: Optional[Member] = None


@dataclass
class Tag(EntityGitlab):
    commit: Commit
    name: str
    message: str
