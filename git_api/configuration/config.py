# -*- coding: utf-8 -*-

"""
Defines :
 The Config class

"""


import dataclasses


@dataclasses.dataclass
class Config:

    """
    A Config holds parameters meant to be shared among all modules of the application.

    Raises
    ------
    ValueError:
        The object self validates at creation time if all its attributes are of the
        correct type, and raises a ValueError if it sees an incoherence.

    """

    root_group_id: str
    access_token: str
    url_base_rest: str
    url_base_graphql: str
    db_suffix: str
    format_date_json: str

    def __post_init__(self) -> None:
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                raise TypeError(
                    f"Expected {field.name} to be {field.type}, " f"got {repr(value)}"
                )
