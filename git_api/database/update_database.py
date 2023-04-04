from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    List,
    runtime_checkable,
    Protocol,
    Optional,
)

if TYPE_CHECKING:
    from git_api.synchronize_with_gitlab import (
        APIProvider,
        JsonParser,
    )
    from git_api.configuration import ConfigProvider
    from git_api.commons.types import GitlabId
    from git_api.commons.entities_gitlab import (
        Group,
        Member,
        Project,
        Branch,
        Commit,
        EntityGitlab,
    )


class DatabaseUpdater:
    def __init__(
        self,
        api_provider: APIProvider,
        json_parser: JsonParser,
        repo_entities: IRepoEntities,
        config_provider: ConfigProvider,
    ):
        self._api_provider = api_provider
        self._json_parser = json_parser
        self._repo_entities = repo_entities
        self._config_provider = config_provider

    def update_all(self) -> None:
        self.update_master_data()
        self.update_transactions()

    def update_master_data(self) -> None:
        master_data_json = self._api_provider.get_master_data_json()
        groups, projects, members = self._json_parser.parse_master_data(
            master_data_json
        )
        for group in groups:
            self._repo_entities.save(group)
        for project in projects:
            self._repo_entities.save(project)
        for member in members:
            self._repo_entities.save(member)
        self._update_branches()

    def update_transactions(self) -> None:
        self._update_commits()
        self._update_tags()

    def _update_branches(self) -> None:
        projects = self._repo_entities.get_projects_all()
        # counter = 1
        for project in projects:
            branch_jsons = self._api_provider.get_branches(project.gitlab_id)
            branches = self._json_parser.parse_branches(branch_jsons)
            for branch in branches:
                branch.gitlab_id = f"{project.gitlab_id}_{branch.name}"
                branch.project = project
                self._repo_entities.save(branch)
            # print(f"{counter} / {len(projects)}")
            # counter += 1

    def _update_commits(self) -> None:
        branches = self._repo_entities.get_branches_all()
        counter = 1
        for branch in branches:
            assert branch.project is not None
            commits_json = self._api_provider.get_commits(
                branch.project.gitlab_id, branch.name
            )
            commits = self._json_parser.parse_commits(commits_json)
            for commit in commits:
                commit.branch = branch
                self._repo_entities.save(commit)
            print(f"{counter} / {len(branches)}")
            counter += 1

    def _update_tags(self) -> None:
        projects = self._repo_entities.get_projects_all()
        counter = 1
        for project in projects:
            tag_jsons = self._api_provider.get_tags(project.gitlab_id)
            tags = self._json_parser.parse_tags(tag_jsons)
            for tag in tags:
                commit = self._repo_entities.get_commit(tag.gitlab_id)
                tag.commit = commit
                self._repo_entities.save(tag)
            print(f"{counter} / {len(projects)}")
            counter += 1


@runtime_checkable
class IRepoEntities(Protocol):
    def save(self, entity: EntityGitlab) -> None:
        ...

    def get_group(self, group_id: GitlabId) -> Optional[Group]:
        ...

    def get_groups_all(self) -> List[Group]:
        ...

    def get_member(self, member_id: GitlabId) -> Optional[Member]:
        ...

    def get_projects_all(self) -> List[Project]:
        ...

    def get_branches_all(self) -> List[Branch]:
        ...

    def get_commit(self, gitlab_id: GitlabId) -> Commit:
        ...

    def get_commits_all(self) -> List[Commit]:
        ...
