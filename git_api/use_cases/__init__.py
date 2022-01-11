from __future__ import annotations

from typing import runtime_checkable, Protocol, Optional, List, TYPE_CHECKING

from .parse_json import JSONParser
from .provide_api import APIProvider
from .provide_config import ConfigProvider, IConfigRepository
from .provide_database import DatabaseProvider, IDatabaseInitializer
from .update_database import DatabaseUpdater
from .manage_git_repository import GitRepositoryManager

if TYPE_CHECKING:
    from entities import Commit, Group, Member, Project
    from git_api.helpers.types import GitlabId


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