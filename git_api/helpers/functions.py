# -*- coding: utf-8 -*-

"""
Defines :
 The get_package_folder method.

 The get_resources_folder method.

"""
import inspect
from pathlib import Path


def get_resources_folder() -> Path:
    """
    The path to the resources folder for my_object.

    The data folder is defined as a sub-folder of the package folder named "resources"
    where my_object is defined. More information is available in the get_package_folder
    documentation.
    If no my_object is passed, returns the resources folder for the package from where
    the function is called.

    """
    package_folder = get_package_folder()
    resources_folder = package_folder / "resources"
    assert resources_folder.exists()
    return resources_folder


def get_package_folder() -> Path:
    """
    The path to the package folder from where the function is called, or where
    my_object is declared.

    If the package has been bundled in a .exe file, returns the folder of the
    application itself. Otherwise, the package folder is defined as the highest folder
    in the folder structure containing an __init__.py file.

    Warnings
    --------
    In the unfrozen case, it is assumed that all package and sub-package have an
    __init__.py file.

    """
    package_path = _get_package_folder_from_caller()
    while _is_parent_a_package(package_path):
        package_path = package_path.parent
    return package_path


def _get_package_folder_from_caller() -> Path:
    index = 0
    caller = inspect.stack()[index].filename
    while caller == __file__:
        index += 1
        caller = inspect.stack()[index].filename
    return Path(caller)


def _is_parent_a_package(package_path: Path) -> bool:
    parent_path = package_path.parent
    init_file = parent_path / "__init__.py"
    return init_file.exists()
