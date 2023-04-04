from typing import List, Dict, Union

from mypy_extensions import TypedDict
from git_api.commons.types import GitlabId

Json = Dict[str, Union[str, int, bytes, Dict[str, Union[str, int, bytes]]]]
JsonTagCommit = TypedDict("JsonTagCommit", {"id": GitlabId})
JsonTag = TypedDict("JsonTag", {"commit": JsonTagCommit, "name": str, "message": str})
JsonBranch = TypedDict(
    "JsonBranch",
    {
        "name": str,
        "default": bool,
        "protected": bool,
        "developers_can_push": bool,
        "developers_can_merge": bool,
        "can_push": bool,
    },
)
JsonCommit = TypedDict(
    "JsonCommit",
    {
        "id": GitlabId,
        "title": str,
        "author_name": str,
        "author_email": str,
        "committed_date": str,
        "message": str,
        "web_url": str,
    },
)
JsonMemberUser = TypedDict("JsonMemberUser", {"id": str, "name": str, "username": str})
JsonMemberAccessLevel = TypedDict("JsonMemberAccessLevel", {"stringValue": str})
JsonMember = TypedDict(
    "JsonMember", {"user": JsonMemberUser, "accessLevel": JsonMemberAccessLevel}
)
JsonProjectRepo = TypedDict("JsonProjectRepo", {"rootRef": str})
JsonProject = TypedDict(
    "JsonProject",
    {
        "id": str,
        "name": str,
        "description": str,
        "webUrl": str,
        "repository": JsonProjectRepo,
        "topics": List[str],
    },
)
JsonGroupMembers = TypedDict("JsonGroupMembers", {"nodes": List[JsonMember]})
JsonGroupProjects = TypedDict("JsonGroupProjects", {"nodes": List[JsonProject]})
JsonGroupDescendants = TypedDict(
    "JsonGroupDescendants", {"nodes": List["JsonGroup"]}  # type: ignore
)
JsonGroup = TypedDict(
    "JsonGroup",
    {
        "id": str,
        "name": str,
        "webUrl": str,
        "description": str,
        "projectCreationLevel": str,
        "projects": JsonGroupProjects,
        "groupMembers": JsonGroupMembers,
        "descendantGroups": JsonGroupDescendants,
    },
)
JsonMasterDataGroup = TypedDict("JsonMasterDataGroup", {"group": JsonGroup})
JsonMasterData = TypedDict("JsonMasterData", {"data": JsonMasterDataGroup})
