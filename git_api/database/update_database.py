from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    List,
    Any,
    runtime_checkable,
    Protocol,
    Optional,
)

if TYPE_CHECKING:
    from git_api.synchronize_with_gitlab import (
        APIProvider,
        JSONParser,
    )
    from git_api.configuration import ConfigProvider
    from git_api.database import IEntitiesRepository
    from git_api.commons.types import GitlabId
    from git_api.commons.entities_gitlab import Group, Member, Project


def iterate_over_root_groups(func: Callable) -> Callable:
    def wrapper(self: Any, *args: List[Any]) -> Any:
        config = self._config_provider.get_config_instance()
        root_group_ids = config.root_group_ids
        for root_group_path in root_group_ids:
            func(self, root_group_path, *args)

    return wrapper


class DatabaseUpdater:
    def __init__(
        self,
        api_provider: APIProvider,
        json_parser: JSONParser,
        entities_repository: IEntitiesRepository,
        config_provider: ConfigProvider,
    ):
        self._api_provider = api_provider
        self._json_parser = json_parser
        self._entities_repository = entities_repository
        self._config_provider = config_provider

    def update_all(self) -> None:
        self.update_master_data()
        self.update_transactions()

    @iterate_over_root_groups
    def update_master_data(self, root_group_path: GitlabId) -> None:
        master_data_json = self._api_provider.get_master_data_json()
        groups, projects, members = self._json_parser.parse_master_data(master_data_json)
        for group in groups:
            self._entities_repository.save_group(group)
        for project in projects:
            self._entities_repository.save_project(project)
        for member in members:
            self._entities_repository.save_member(member)
        self._update_branches()

    def update_transactions(self) -> None:
        self._update_commits()
        self._update_tags()

    def _update_branches(self) -> None:
        projects = self._entities_repository.get_projects_all()
        counter = 1
        for project in projects:
            branch_jsons = self._api_provider.get_branches(project.gitlab_id)
            branches = self._json_parser.parse_branches(branch_jsons)
            for branch in branches:
                branch.gitlab_id = f"{project.gitlab_id}_{branch.name}"
                branch.project = project
                self._entities_repository.save_branch(branch)
            print(f"{counter} / {len(projects)}")
            counter += 1

    def _update_commits(self) -> None:
        branches = self._entities_repository.get_branches_all()
        counter = 1
        for branch in branches:
            commits_json = self._api_provider.get_commits(branch.project.gitlab_id, branch.name)
            commits = self._json_parser.parse_commits(commits_json)
            for commit in commits:
                commit.branch = branch
                self._entities_repository.save_commit(commit)
            print(f"{counter} / {len(branches)}")
            counter += 1

    def _update_tags(self) -> None:
        projects = self._entities_repository.get_projects_all()
        counter = 1
        for project in projects:
            tag_jsons = self._api_provider.get_tags(project.gitlab_id)
            tags = self._json_parser.parse_tags(tag_jsons)
            for tag in tags:
                commit = self._entities_repository.get_commit(tag.gitlab_id)
                tag.commit = commit
                self._entities_repository.save_tag(tag)
            print(f"{counter} / {len(projects)}")
            counter += 1


@runtime_checkable
class IEntitiesRepository(Protocol):
    def save(self, group: Group) -> None:
        ...

    def get_group_by_id(self, group_id: GitlabId) -> Optional[Group]:
        ...

    def get_groups_all(self) -> List[Group]:
        ...

    def get_member_by_id(self, member_id: GitlabId) -> Optional[Member]:
        ...

    def get_projects_all(self) -> List[Project]:
        ...
