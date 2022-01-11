from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git_api.use_cases import IEntitiesRepository, APIProvider


class GitRepositoryManager:

    def __init__(self, entities_repository: IEntitiesRepository, api_provider: APIProvider):
        self._entities_repository = entities_repository
        self._api_provider = api_provider

    def protect_all_default_branches(self):
        for project in self._entities_repository.get_projects_all():
            self._api_provider.modify_branch_protection(
                project.gitlab_id, project.default_branch, 0, 30
            )
