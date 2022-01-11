from pathlib import Path

from ruamel.yaml import YAML

from configuration.config import Config
from commons.functions import get_resources_folder
from git_api.use_cases import IConfigRepository


class ConfigRepoYaml:

    """
    ConfigYamlRepository implements both IConfigRepositoryLoader and
    IConfigRepositoryModifier. It uses ruamel.yaml and stores the configuration in a
    .yaml file.

    Ruamel.yaml allows to keep the comments and general formatting of the
    pre-existing .yaml file when saving new values. The actual data, including the
    information about the comments and formatting are stored in a private attribute
    _data.

    """

    def __init__(self) -> None:
        self._config_file_path: Path = self._get_config_file_path()
        assert isinstance(self, IConfigRepository)

    def load(self) -> Config:
        """See IConfigRepositoryLoader documentation."""
        data_config = YAML().load(self._config_file_path)
        assert data_config is not None
        config = Config(**data_config)
        return config

    @staticmethod
    def _get_config_file_path() -> Path:
        config_file_path = get_resources_folder() / "config.yaml"
        return config_file_path
