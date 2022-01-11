import pytest

from git_api.entities import Branch, Commit, Group, Member


@pytest.fixture
def mock_member(
    mock_gitlab_ids, mock_member_user_name, mock_member_name, mock_member_role
):
    return Member(
        mock_gitlab_ids, mock_member_user_name, mock_member_name, mock_member_role
    )


@pytest.fixture
def mock_group_root(
    mock_gitlab_ids,
    mock_group_name,
    mock_group_url,
    mock_group_description,
    mock_group_project_creation_level,
):
    return Group(
        mock_gitlab_ids[1],
        mock_group_name,
        mock_group_url,
        mock_group_description,
        mock_group_project_creation_level,
        None,
    )


@pytest.fixture
def mock_group_root_child(
    mock_gitlab_ids,
    mock_group_name_child,
    mock_group_url_child,
    mock_group_description_child,
    mock_group_project_creation_level,
        mock_group_root,
):
    return Group(
        mock_gitlab_ids[2],
        mock_group_name_child,
        mock_group_url_child,
        mock_group_description_child,
        mock_group_project_creation_level,
        mock_group_root,
    )


# @pytest.fixture
# def mock_commit(
#     mock_gitlab_ids,
#     mock_commit_title,
#     mock_commit_author_name,
#     mock_commit_author_email,
#     mock_commit_date,
#     mock_commit_message,
#     mock_commit_url,
#     mock_branch,
#     mock_member,
# ):
#     return Commit(
#         mock_gitlab_ids[0],
#         mock_commit_title,
#         mock_commit_author_name,
#         mock_commit_author_email,
#         mock_commit_date,
#         mock_commit_message,
#         mock_commit_url,
#         mock_branch,
#         mock_member,
#     )
