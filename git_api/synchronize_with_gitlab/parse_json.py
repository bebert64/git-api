from __future__ import annotations

from git_api.commons.entities_gitlab import Branch, Commit, Group, Member, Project, Tag


class JSONParser:

    access_level_to_role = {
        0: "No access",
        5: "Minimal access",
        10: "Guest",
        20: "Reporter",
        30: "Developer",
        40: "Maintainer",
        50: "Owner",
    }

    def parse_master_data(self, master_data_json):
        data_root_group = master_data_json["data"]["group"]
        members = self._parse_members(data_root_group)
        groups, projects = self._parse_groups_and_projects(data_root_group, None)
        return groups, projects, members

    def _parse_groups_and_projects(self, data_group, parent):
        groups = []
        root_group = self._parse_group(data_group, parent)
        groups.append(root_group)
        projects = self._parse_projects(data_group, root_group)
        groups, projects = self._parse_subgroups(
            data_group, root_group, groups, projects
        )
        return groups, projects

    @staticmethod
    def _parse_group(data_group, parent):
        return Group(
            gitlab_id=int(data_group["id"].split("/")[-1]),
            name=data_group["name"],
            web_url=data_group["webUrl"],
            description=data_group["description"],
            project_creation_level=data_group["projectCreationLevel"],
            parent=parent
        )

    def _parse_projects(self, data_group, root_group):
        projects = []
        for data_project in data_group["projects"]["nodes"]:
            project = self._parse_project(data_project, root_group)
            projects.append(project)
        return projects

    def _parse_subgroups(self, data_group, root_group, groups, projects):
        try:
            data_descendants = data_group["descendantGroups"]["nodes"]
        except KeyError:
            pass
        else:
            for data_group_child in data_descendants:
                groups_child, projects_child = self._parse_groups_and_projects(
                    data_group_child, root_group)
                groups += groups_child
                projects += projects_child
        return groups, projects

    @staticmethod
    def _parse_project(data_project, root_group):
        project = Project(
            gitlab_id=int(data_project["id"].split("/")[-1]),
            name=data_project["name"],
            description=data_project["description"],
            web_url=data_project["webUrl"],
            default_branch=data_project["repository"]["rootRef"],
            topics=", ".join(data_project["topics"]),
            group=root_group,
        )
        return project

    def _parse_members(self, data_root_group):
        data_members = data_root_group["groupMembers"]["nodes"]
        members = []
        for data_member in data_members:
            member = self._parse_member(data_member)
            members.append(member)
        return members

    @staticmethod
    def _parse_member(data_member):
        return Member(
            gitlab_id=int(data_member["user"]["id"].split("/")[-1]),
            name=data_member["user"]["name"],
            username=data_member["user"]["username"],
            role=data_member["accessLevel"]["stringValue"].lower(),
        )

    @staticmethod
    def parse_commits(commits_json):
        commits = []
        for commit_json in commits_json:
            commit = JSONParser._parse_commit(commit_json)
            commits.append(commit)
        return commits

    @staticmethod
    def _parse_commit(commit_json):
        return Commit(
            gitlab_id=commit_json["id"],
            title=commit_json["title"],
            author_name=commit_json["author_name"],
            author_email=commit_json["author_email"],
            committed_date=commit_json["committed_date"][:10],
            message=commit_json["message"],
            web_url=commit_json["web_url"],
            branch="",
            member=None,
        )

    @staticmethod
    def parse_branches(branch_jsons):
        branches = []
        for branch_json in branch_jsons:
            branch = JSONParser._parse_branch(branch_json)
            branches.append(branch)
        return branches

    @staticmethod
    def _parse_branch(branch_json):
        return Branch(
            gitlab_id="",
            name=branch_json["name"],
            project=None,
            is_default=branch_json["default"],
            is_protected=branch_json["protected"],
            developers_can_push=branch_json["developers_can_push"],
            developers_can_merge=branch_json["developers_can_merge"],
            can_push=branch_json["can_push"],
        )

    @staticmethod
    def parse_tags(tag_jsons):
        tags = []
        for tag_json in tag_jsons:
            tag = JSONParser._parse_tag(tag_json)
            tags.append(tag)
        return tags

    @staticmethod
    def _parse_tag(tag_json):
        return Tag(
            gitlab_id=tag_json["commit"]["id"],
            commit=tag_json["commit"]["id"],
            name=tag_json["name"],
            message=tag_json["message"],
        )
