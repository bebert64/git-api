# -*- coding: utf-8 -*-

"""Defines the Dependencies class."""

from __future__ import annotations

from git_api.configuration import (
    ConfigRepoYaml,
    ConfigProvider,
    IConfigRepository,
)
from git_api.database import (
    EntitiesRepoPeewee,
    DatabaseInitializerPeewee,
    DatabaseProvider,
    IDatabaseInitializer,
    DatabaseUpdater,
    IEntitiesRepository,
)
from git_api.synchronize_with_gitlab import (
    APIProvider,
    JSONParser,
    GitRepositoryManager,
)


class Dependencies:

    """
    The Dependencies class is a basic holder for all dependencies needed to be injected
    anywhere in the application.

    To implement the Dependency Injection pattern, and to avoid using yet another
    external library, we create all dependencies once and inject them in the
    main ui component at the very beginning of the execution.
    All the Presenters, Interactors and other dependencies are instantiated inside the
    __init__method and can then be injected anywhere needed.

    It also helps to have a single entry point where one can define which dependencies
    (which libraries or platform specific classes) will be used for this version
    of the program).

    """

    # pylint: disable=too-many-instance-attributes, too-few-public-methods

    def __init__(self) -> None:
        # Create config-related objects
        self.config_repo: IConfigRepository = ConfigRepoYaml()
        self.config_provider = ConfigProvider(self.config_repo)

        # Create repositories
        self.entities_repo: IEntitiesRepository = EntitiesRepoPeewee()

        # Create interactors
        self.database_initializer: IDatabaseInitializer = DatabaseInitializerPeewee()
        self.database_provider = DatabaseProvider(
            self.database_initializer, self.config_provider
        )
        self.api_provider = APIProvider(self.config_provider)
        self.json_parser = JSONParser()
        self.database_updater = DatabaseUpdater(
            self.api_provider,
            self.json_parser,
            self.entities_repo,
            self.config_provider,
        )
        self.git_repository_manager = GitRepositoryManager(
            self.entities_repo, self.api_provider
        )
