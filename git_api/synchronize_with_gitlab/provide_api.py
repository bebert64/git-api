from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Dict, cast

import requests

from .query_graphql import QUERY_GRAPHQL as query_graphql_raw
from .types import JsonMasterData, JsonCommit, JsonTag, JsonBranch, Json

if TYPE_CHECKING:
    from git_api.configuration import ConfigProvider
    from git_api.commons.types import GitlabId


class APIProvider:
    def __init__(self, config_provider: ConfigProvider):
        self._config_provider = config_provider
        self._session = requests.Session()
        self._init_session()

    def get_master_data_json(self) -> JsonMasterData:
        self._init_graphql()
        config = self._config_provider.get_config_instance()
        print("launching request, please wait")
        master_data_json = self._session.post(
            config.url_base_graphql, json={"query": self._get_query_graphql()}
        ).json()
        print("data retrieved")
        return cast(JsonMasterData, master_data_json)

    def get_commits(self, project_id: GitlabId, branch_name: str) -> List[JsonCommit]:
        self._init_rest()
        end_point_url = f"projects/{project_id}/repository/commits"
        data = {"ref_name": branch_name}
        return cast(List[JsonCommit], self._get_response_json(end_point_url, data))

    def get_tags(self, project_id: GitlabId) -> List[JsonTag]:
        end_point_url = f"projects/{project_id}/repository/tags"
        return cast(List[JsonTag], self._get_response_json(end_point_url))

    def get_branches(self, project_id: GitlabId) -> List[JsonBranch]:
        end_point_url = f"projects/{project_id}/repository/branches"
        return cast(List[JsonBranch], self._get_response_json(end_point_url))

    def get_protected_branches(self, project_id: GitlabId) -> List[JsonBranch]:
        end_point_url = f"projects/{project_id}/protected_branches"
        return cast(List[JsonBranch], self._get_response_json(end_point_url))

    def modify_branch_protection(
        self,
        project_id: GitlabId,
        branch_name: str,
        push_access_level: str,
        merge_access_level: str,
    ) -> None:
        self._delete_protected_branch(project_id, branch_name)
        self._create_protected_branch(
            project_id, branch_name, push_access_level, merge_access_level
        )

    def _init_graphql(self) -> None:
        self._session = requests.Session()
        config = self._config_provider.get_config_instance()
        token = config.access_token
        self._session.headers.update({"Authorization": f"Bearer {token}"})
        self._session.headers.update({"Content-Type": "application/json"})

    def _init_rest(self) -> None:
        self._session = requests.Session()
        config = self._config_provider.get_config_instance()
        token = config.access_token
        self._session.headers.update({"PRIVATE-TOKEN": token})

    def _create_protected_branch(
        self,
        project_id: GitlabId,
        branch_name: str,
        push_access_level: str,
        merge_access_level: str,
    ) -> None:
        end_point_url = f"projects/{project_id}/protected_branches"
        url_request = self._build_url(end_point_url)
        self._session.post(
            url_request,
            data={
                "name": branch_name,
                "push_access_level": push_access_level,
                "merge_access_level": merge_access_level,
            },
        )

    def _delete_protected_branch(self, project_id: GitlabId, branch_name: str) -> None:
        end_point_url = f"projects/{project_id}/protected_branches/{branch_name}"
        url_request = self._build_url(end_point_url)
        self._session.delete(url_request)

    def _init_session(self) -> None:
        config = self._config_provider.get_config_instance()
        token = config.access_token
        self._session.headers.update({"PRIVATE-TOKEN": token})

    def _build_url(self, end_point_url: str) -> str:
        config = self._config_provider.get_config_instance()
        return config.url_base_rest + end_point_url

    def _get_response_json(
        self, end_point_url: str, data: Optional[Dict[str, str]] = None
    ) -> Json:
        url_request = self._build_url(end_point_url)
        if data is None:
            data = {}
        api_response = self._session.get(url_request, data=data)
        return cast(Json, api_response.json())

    def _get_query_graphql(self) -> str:
        config = self._config_provider.get_config_instance()
        query = query_graphql_raw.replace("{{root_group_id}}", config.root_group_id)
        return query
