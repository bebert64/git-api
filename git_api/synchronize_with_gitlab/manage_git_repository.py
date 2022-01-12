from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git_api.database import IRepoEntities
    from git_api.synchronize_with_gitlab import APIProvider


class GitRepositoryManager:
    def __init__(
        self, repo_entities: IRepoEntities, api_provider: APIProvider
    ):
        self._repo_entities = repo_entities
        self._api_provider = api_provider

    def protect_all_default_branches(self) -> None:
        for project in self._repo_entities.get_projects_all():
            self._api_provider.modify_branch_protection(
                project.gitlab_id, project.default_branch, 0, 30
            )
