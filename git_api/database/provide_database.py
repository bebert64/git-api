from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Optional, Protocol, runtime_checkable

from commons.functions import get_package_folder


class DatabaseProvider:
    def __init__(self, database_initializer: IDatabaseInitializer):
        self.database_path: Optional[Path] = None
        self._database_initializer = database_initializer

    def set_up_db(self):
        db_path = self._get_argv_database_path()
        if db_path is None:
            db_path = self._get_empty_database_path()
            db_path.unlink(missing_ok=True)
            self._database_initializer.create_empty_database(db_path)
        else:
            self._database_initializer.init_db(db_path)

    def save_as(self, db_path: Path) -> None:
        shutil.copy(self.database_path, db_path)
        self._database_initializer.reconnect(db_path)

    def _get_argv_database_path(self) -> Optional[Path]:
        try:
            self.database_path = Path(sys.argv[1])
        except IndexError:
            self.database_path = None
        else:
            if not self.database_path.exists() or self.database_path.suffix != ".gadb":
                self.database_path = None
        return self.database_path

    def _get_empty_database_path(self):
        self.database_path = get_package_folder() / "db_temp.gadb"
        return self.database_path


@runtime_checkable
class IDatabaseInitializer(Protocol):
    def init_db(self, db_path: Path) -> None:
        ...

    def create_empty_database(self, db_path: Path) -> None:
        ...

    def reconnect(self, db_path: Path) -> None:
        ...
