from __future__ import annotations

from typing import Optional, List, Dict, Type, cast, overload, Any

from git_api.commons.entities_gitlab import (
    EntityGitlab,
    Branch,
    Commit,
    Group,
    Member,
    Project,
    Tag,
)
from git_api.commons.types import GitlabId
from .models import (
    CommitModel,
    GroupModel,
    MemberModel,
    ProjectModel,
    TagModel,
    BaseModel,
    BranchModel,
)

from ..update_database import IRepoEntities


class RepoEntitiesPeewee:

    _dict_entity_model: Dict[Type[EntityGitlab], Type[BaseModel]] = {
        Commit: CommitModel,
        Group: GroupModel,
        Member: MemberModel,
        Project: ProjectModel,
        Tag: TagModel,
        Branch: BranchModel,
    }

    _dict_model_entity: Dict[Type[BaseModel], Type[EntityGitlab]] = {
        Model: Entity for Entity, Model in _dict_entity_model.items()
    }

    def __init__(self) -> None:
        assert isinstance(self, IRepoEntities)

    @staticmethod
    def get_group(group_id: GitlabId) -> Optional[Group]:
        group_model = GroupModel.get_or_none(gitlab_id=group_id)
        return cast(Optional[Group], RepoEntitiesPeewee._model_to_entity(group_model))

    @staticmethod
    def get_groups_all() -> List[Group]:
        group_models_all = GroupModel.select()
        return cast(
            List[Group],
            [
                RepoEntitiesPeewee._model_to_entity(group_model)
                for group_model in group_models_all
            ],
        )

    @staticmethod
    def get_member(member_id: GitlabId) -> Optional[Member]:
        member_model = MemberModel.get_or_none(gitlab_id=member_id)
        return cast(Optional[Member], RepoEntitiesPeewee._model_to_entity(member_model))

    @staticmethod
    def get_projects_all() -> List[Project]:
        project_models_all = ProjectModel.select()
        return cast(
            List[Project],
            [
                RepoEntitiesPeewee._model_to_entity(project_model)
                for project_model in project_models_all
            ],
        )

    @staticmethod
    def get_branches_all() -> List[Branch]:
        branch_models_all = BranchModel.select()
        return cast(
            List[Branch],
            [
                RepoEntitiesPeewee._model_to_entity(branch_model)
                for branch_model in branch_models_all
            ],
        )

    @staticmethod
    def get_commit(gitlab_id: GitlabId) -> Commit:
        commit_model = CommitModel.get(CommitModel.gitlab_id == gitlab_id)
        return cast(Commit, RepoEntitiesPeewee._model_to_entity(commit_model))

    @staticmethod
    def get_commits_all() -> List[Commit]:
        commit_models_all = CommitModel.select()
        return cast(
            List[Commit],
            [
                RepoEntitiesPeewee._model_to_entity(commit_model)
                for commit_model in commit_models_all
            ],
        )

    @staticmethod
    def save(entity: EntityGitlab) -> None:
        model_type = RepoEntitiesPeewee._dict_entity_model[type(entity)]
        model = model_type.get_or_none(gitlab_id=entity.gitlab_id)
        force_insert = False
        if model is None:
            model = model_type()
            force_insert = True
        for (
            field
        ) in model_type._meta.sorted_field_names:  # pylint: disable=protected-access
            field_value = getattr(entity, field)
            if isinstance(field_value, EntityGitlab):
                field_value = field_value.gitlab_id
            setattr(model, field, field_value)
        model.save(force_insert=force_insert)

    @overload
    @staticmethod
    def _model_to_entity(model: None) -> None:
        ...

    @overload
    @staticmethod
    def _model_to_entity(model: BaseModel) -> EntityGitlab:
        ...

    @staticmethod
    def _model_to_entity(model: Optional[BaseModel]) -> Optional[EntityGitlab]:
        if model is None:
            entity = None
        else:
            model_type = type(model)
            entity_type = RepoEntitiesPeewee._dict_model_entity[model_type]
            entity_data = RepoEntitiesPeewee._get_entity_data(model)
            entity = entity_type(**entity_data)
        return entity

    @staticmethod
    def _get_entity_data(model: BaseModel) -> Dict[str, Any]:
        entity_data: Dict[str, Any] = {}
        model_type = type(model)
        for (
            field
        ) in model_type._meta.sorted_field_names:  # pylint: disable=protected-access
            field_value = getattr(model, field)
            if isinstance(field_value, BaseModel):
                field_value = RepoEntitiesPeewee._model_to_entity(field_value)
            entity_data[field] = field_value
        return entity_data
