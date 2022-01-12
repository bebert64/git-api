from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable, TYPE_CHECKING

from git_api.commons.functions import get_package_folder

if TYPE_CHECKING:
    from git_api.configuration import ConfigProvider


class DatabaseProvider:
    def __init__(
        self,
        database_initializer: IDatabaseInitializer,
        config_provider: ConfigProvider,
    ):
        self.database_path: Optional[Path] = None
        self._database_initializer = database_initializer
        self._config_provider = config_provider

    def set_up_db(self) -> None:
        db_path = self._get_argv_database_path()
        if db_path is None:
            db_path = self._get_empty_database_path()
            db_path.unlink(missing_ok=True)
            self._database_initializer.create_empty_database(db_path)
        else:
            self._database_initializer.init_and_connect_db(db_path)

    def save_as(self, db_path: Path) -> None:
        assert self.database_path is not None
        shutil.copy(self.database_path, db_path)
        self._database_initializer.reconnect(db_path)

    def _get_argv_database_path(self) -> Optional[Path]:
        try:
            self.database_path = Path(sys.argv[1])
        except IndexError:
            self.database_path = None
        else:
            config = self._config_provider.get_config_instance()
            if (
                not self.database_path.exists()
                or self.database_path.suffix != config.db_suffix
            ):
                self.database_path = None
        return self.database_path

    def _get_empty_database_path(self) -> Path:
        self.database_path = get_package_folder() / "db_temp.gadb"
        return self.database_path


@runtime_checkable
class IDatabaseInitializer(Protocol):
    def init_and_connect_db(self, db_path: Path) -> None:
        ...

    def create_empty_database(self, db_path: Path) -> None:
        ...

    def reconnect(self, db_path: Path) -> None:
        ...
