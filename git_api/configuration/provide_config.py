# -*- coding: utf-8 -*-

"""
Defines the ConfigProvider class, and the IConfigRepositoryProtocol.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .config import Config


class ConfigProvider:

    """
    The ConfigProvider role is to give access to the Config singleton.
    """

    def __init__(self, config_repository: IConfigRepository):
        self._config_repository = config_repository

    def get_config_instance(self) -> Config:
        """Returns the Config singleton."""
        return self._config_repository.load()


@runtime_checkable
class IConfigRepository(Protocol):

    """
    IConfigRepository is the protocol that must be implemented by a concrete
    implementation of any configuration file repository.
    """

    def load(self) -> Config:
        """
        Loads data from the configuration repository and returns the corresponding
        Config object.
        """
