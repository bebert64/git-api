from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Tuple

from git_api.commons.entities_gitlab import Branch, Commit, Group, Member, Project, Tag

if TYPE_CHECKING:
    from .types import (
        JsonTag,
        JsonBranch,
        JsonCommit,
        JsonMember,
        JsonGroup,
        JsonMasterData,
        JsonProject,
    )
    from git_api.configuration import ConfigProvider


class JsonParser:

    access_level_to_role = {
        0: "No access",
        5: "Minimal access",
        10: "Guest",
        20: "Reporter",
        30: "Developer",
        40: "Maintainer",
        50: "Owner",
    }

    def __init__(self, config_provider: ConfigProvider):
        self._config_provider = config_provider

    def parse_master_data(
        self, json_master_data: JsonMasterData
    ) -> Tuple[List[Group], List[Project], List[Member]]:
        json_group = json_master_data["data"]["group"]
        json_members = json_group["groupMembers"]["nodes"]
        members = self._parse_members(json_members)
        groups, projects = self._parse_groups_and_projects(json_group, None)
        return groups, projects, members

    def _parse_groups_and_projects(
        self, json_group: JsonGroup, group_parent: Optional[Group]
    ) -> Tuple[List[Group], List[Project]]:
        group_root = self._parse_group(json_group, group_parent)
        groups = [group_root]
        json_projects = json_group["projects"]["nodes"]
        projects = self._parse_projects(json_projects, group_root)
        groups, projects = self._parse_subgroups(
            json_group, group_root, groups, projects
        )
        return groups, projects

    @staticmethod
    def _parse_group(json_group: JsonGroup, group_parent: Optional[Group]) -> Group:
        return Group(
            gitlab_id=json_group["id"].split("/")[-1],
            name=json_group["name"],
            web_url=json_group["webUrl"],
            description=json_group["description"],
            project_creation_level=json_group["projectCreationLevel"],
            parent=group_parent,
        )

    def _parse_projects(
        self, json_projects: List[JsonProject], group: Group
    ) -> List[Project]:
        projects = []
        for json_project in json_projects:
            project = self._parse_project(json_project, group)
            projects.append(project)
        return projects

    def _parse_subgroups(
        self,
        json_group: JsonGroup,
        group_root: Group,
        groups: List[Group],
        projects: List[Project],
    ) -> Tuple[List[Group], List[Project]]:
        try:
            json_descendants = json_group["descendantGroups"]["nodes"]
        except KeyError:
            pass
        else:
            for json_group_child in json_descendants:
                groups_child, projects_child = self._parse_groups_and_projects(
                    json_group_child, group_root
                )
                groups += groups_child
                projects += projects_child
        return groups, projects

    @staticmethod
    def _parse_project(json_project: JsonProject, group: Group) -> Project:
        project = Project(
            gitlab_id=json_project["id"].split("/")[-1],
            name=json_project["name"],
            description=json_project["description"],
            web_url=json_project["webUrl"],
            default_branch=json_project["repository"]["rootRef"],
            topics=", ".join(json_project["topics"]),
            group=group,
        )
        return project

    def _parse_members(self, json_members: List[JsonMember]) -> List[Member]:
        members = []
        for json_member in json_members:
            member = self._parse_member(json_member)
            members.append(member)
        return members

    @staticmethod
    def _parse_member(json_member: JsonMember) -> Member:
        return Member(
            gitlab_id=json_member["user"]["id"].split("/")[-1],
            name=json_member["user"]["name"],
            username=json_member["user"]["username"],
            role=json_member["accessLevel"]["stringValue"].lower(),
        )

    def parse_commits(self, json_commits: List[JsonCommit]) -> List[Commit]:
        commits = []
        for json_commit in json_commits:
            commit = self._parse_commit(json_commit)
            commits.append(commit)
        return commits

    def _parse_commit(self, json_commit: JsonCommit) -> Commit:
        config = self._config_provider.get_config_instance()
        return Commit(
            gitlab_id=json_commit["id"],
            title=json_commit["title"],
            author_name=json_commit["author_name"],
            author_email=json_commit["author_email"],
            committed_date=datetime.strptime(
                json_commit["committed_date"][:10], config.format_date_json
            ),
            message=json_commit["message"],
            web_url=json_commit["web_url"],
            branch=None,
            member=None,
        )

    @staticmethod
    def parse_branches(json_branch: List[JsonBranch]) -> List[Branch]:
        branches = []
        for branch_json in json_branch:
            branch = JsonParser._parse_branch(branch_json)
            branches.append(branch)
        return branches

    @staticmethod
    def _parse_branch(json_branch: JsonBranch) -> Branch:
        return Branch(
            gitlab_id="-1",
            name=json_branch["name"],
            project=None,
            is_default=json_branch["default"],
            is_protected=json_branch["protected"],
            developers_can_push=json_branch["developers_can_push"],
            developers_can_merge=json_branch["developers_can_merge"],
            can_push=json_branch["can_push"],
        )

    @staticmethod
    def parse_tags(json_tags: List[JsonTag]) -> List[Tag]:
        tags = []
        for json_tag in json_tags:
            tag = JsonParser._parse_tag(json_tag)
            tags.append(tag)
        return tags

    @staticmethod
    def _parse_tag(json_tag: JsonTag) -> Tag:
        commit = Commit(gitlab_id=json_tag["commit"]["id"],)
        return Tag(
            gitlab_id=json_tag["commit"]["id"],
            commit=commit,
            name=json_tag["name"],
            message=json_tag["message"],
        )
