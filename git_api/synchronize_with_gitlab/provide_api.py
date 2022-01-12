from __future__ import annotations

import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git_api.configuration import ConfigProvider


class APIProvider:
    def __init__(self, config_provider: ConfigProvider):
        self._config_provider = config_provider
        self._session = requests.Session()
        self._init_session()

    def get_master_data_json(self):
        url = self._init_graphql()
        print("launching request, please wait")
        master_data_json = self._session.post(url, json={"query": query_test}).json()
        print("data retrieved")
        return master_data_json

    def get_commits(self, project_id, branch_name):
        self._init_rest()
        end_point_url = f"projects/{project_id}/repository/commits"
        data = {"ref_name": branch_name}
        return self._get_response_json(end_point_url, data)

    def get_tags(self, project_id):
        end_point_url = f"projects/{project_id}/repository/tags"
        return self._get_response_json(end_point_url)

    def get_branches(self, project_id):
        end_point_url = f"projects/{project_id}/repository/branches"
        return self._get_response_json(end_point_url)

    def get_protected_branches(self, project_id):
        end_point_url = f"projects/{project_id}/protected_branches"
        protected_branches_json = self._get_response_json(end_point_url)
        return protected_branches_json

    def modify_branch_protection(
        self, project_id, branch_name, push_access_levels, merge_access_level
    ):
        self._delete_protected_branch(project_id, branch_name)
        self._create_protected_branch(
            project_id, branch_name, push_access_levels, merge_access_level
        )

    def _init_graphql(self) -> None:
        url = "https://gitlab.com/api/graphql"
        self._session = requests.Session()
        config = self._config_provider.get_config_instance()
        token = config.access_token
        self._session.headers.update({"Authorization": f"Bearer {token}"})
        self._session.headers.update({"Content-Type": "application/json"})
        return url

    def _init_rest(self) -> None:
        self._session = requests.Session()
        config = self._config_provider.get_config_instance()
        token = config.access_token
        self._session.headers.update({"PRIVATE-TOKEN": token})

    def _create_protected_branch(
        self, project_id, branch_name, push_access_level, merge_access_level
    ) -> None:
        end_point_url = f"projects/{project_id}/protected_branches"
        url_request = self._build_url(end_point_url)
        self._session.post(
            url_request,
            data={
                "name": branch_name,
                "push_access_level": str(push_access_level),
                "merge_access_level": str(merge_access_level),
            },
        )

    def _delete_protected_branch(self, project_id, branch_name) -> None:
        end_point_url = f"projects/{project_id}/protected_branches/{branch_name}"
        url_request = self._build_url(end_point_url)
        self._session.delete(url_request)

    def _init_session(self) -> None:
        config = self._config_provider.get_config_instance()
        token = config.access_token
        self._session.headers.update({"PRIVATE-TOKEN": token})

    def _build_url(self, end_point_url: str) -> str:
        config = self._config_provider.get_config_instance()
        return config.url_base + end_point_url

    def _get_response_json(self, end_point_url, data=None):
        url_request = self._build_url(end_point_url)
        if data is None:
            data = {}
        api_response = self._session.get(url_request, data=data)
        return api_response.json()


query_test = """
fragment MemberFields on Group {
    groupMembers {
        nodes {
            accessLevel {
                stringValue
            }
            user {
                id
                name
                username
            }
        }
    }
}

fragment GroupFields on Group {
    id
    name
    webUrl
    description
    projectCreationLevel
    projects {
        nodes {
            id
            name
            description
            webUrl
            topics
            repository {
                rootRef
            }
        }
    }
}

fragment GroupsRecursive on Group {
    descendantGroups {
        nodes {
            ...GroupFields
            descendantGroups {
                nodes {
                    ...GroupFields
                }
            }
        }
    }
}

{
    group(fullPath: "autajon_etudes") {
        ...GroupFields
        ...MemberFields
        ...GroupsRecursive
    }
}
"""
