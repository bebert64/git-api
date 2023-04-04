from datetime import date

import pytest


@pytest.fixture
def mock_gitlab_ids():
    return list(range(100))


@pytest.fixture
def mock_member_user_name():
    return "user_name"


@pytest.fixture
def mock_member_name():
    return "Member's name"


@pytest.fixture
def mock_member_role():
    return "Developer"


@pytest.fixture
def mock_group_name():
    return "Group name"


@pytest.fixture
def mock_group_url():
    return "http://my.group.url"


@pytest.fixture
def mock_group_description():
    return "Group Description"


@pytest.fixture
def mock_group_name_child():
    return "Group name child"


@pytest.fixture
def mock_group_url_child():
    return "http://my.group.url/child"


@pytest.fixture
def mock_group_description_child():
    return "Group Description child"


@pytest.fixture
def mock_group_project_creation_level():
    return "Developer"


@pytest.fixture
def mock_commit_title():
    return "commit title"


@pytest.fixture
def mock_commit_author_name():
    return "commit author name"


@pytest.fixture
def mock_commit_author_email():
    return "email@author.net"


@pytest.fixture
def mock_commit_date():
    return date(2020, 9, 1)


@pytest.fixture
def mock_commit_message():
    return "commit message  "


@pytest.fixture
def mock_commit_url():
    return "http://my.commit.url"