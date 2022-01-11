from __future__ import annotations

from typing import Optional, List

from git_api.entities import GitEntity
from entities import Branch, Commit, Group, Member, Project, Tag
from commons.types import GitlabId
from .models import (
    CommitModel,
    GroupModel,
    MemberModel,
    ProjectModel,
    TagModel,
    BaseModel,
    BranchModel,
)

from git_api.use_cases import IEntitiesRepository


class EntitiesRepoPeewee:

    _entity_to_model = {
        Commit: CommitModel,
        Group: GroupModel,
        Member: MemberModel,
        Project: ProjectModel,
        Tag: TagModel,
        Branch: BranchModel,
    }

    _model_to_entity = {Model: Entity for Entity, Model in _entity_to_model.items()}

    def __init__(self) -> None:
        assert isinstance(self, IEntitiesRepository)

    def get_group_by_id(self, group_id: GitlabId) -> Optional[Group]:
        group_model = GroupModel.get_or_none(gitlab_id=group_id)
        return self._get_entity(group_model)

    def get_groups_all(self) -> List[Group]:
        group_models_all = GroupModel.select()
        return [self._get_entity(group_model) for group_model in group_models_all]

    # def save_group(self, group: Group) -> None:
    #     group_parent = group.parent
    #     if group_parent is not None and self.get_group_by_id(group_parent.gitlab_id) is None:
    #         print(f"Impossible to save Group {group.name}, because parent Group ({group_parent.gitlab_id}) hasn't been created yet.")
    #     else:
    #         self.save(group)

    def get_member_by_id(self, member_id: GitlabId) -> Optional[Group]:
        member_model = MemberModel.get_or_none(gitlab_id=member_id)
        return self._get_entity(member_model)

    def get_projects_all(self) -> List[Project]:
        project_models_all = ProjectModel.select()
        return [self._get_entity(project_model) for project_model in project_models_all] 

    def get_branches_all(self) -> List[Branch]:
        branch_models_all = BranchModel.select()
        # return [self._get_branch(branch_model) for branch_model in branch_models_all] 
        return [self._get_entity(branch_model) for branch_model in branch_models_all] 

    def get_commit(self, gitlab_id) -> Commit:
        commit_model = CommitModel.get(CommitModel.gitlab_id == gitlab_id)
        return self._get_entity(commit_model)

    def get_commits_all(self) -> List[Commit]:
        commit_models_all = CommitModel.select()
        return [self._get_entity(commit_model) for commit_model in commit_models_all] 

    @staticmethod
    def save(entity: Entity) -> None:
        model_type = EntitiesRepoPeewee._entity_to_model[type(entity)]
        model = model_type.get_or_none(gitlab_id=entity.gitlab_id)
        force_insert = False
        if model is None:
            model = model_type()
            force_insert = True
        for field in model_type._meta.sorted_field_names:
            field_value = getattr(entity, field)
            if isinstance(field_value, GitEntity):
                field_value = field_value.gitlab_id
            setattr(model, field, field_value)
        model.save(force_insert=force_insert)

    @staticmethod
    def _get_entity(model: Optional[BaseModel]) -> Optional[Entity]:
        if model is None:
            entity = None
        else:
            entity_type = EntitiesRepoPeewee._model_to_entity[type(model)]
            model_type = type(model)
            entity_data = {}
            for field in model_type._meta.sorted_field_names:
                field_value = getattr(model, field)
                if isinstance(field_value, BaseModel):
                    field_value = EntitiesRepoPeewee._get_entity(field_value)
                entity_data[field] = field_value
            entity = entity_type(**entity_data)
        return entity

    # def _get_branch(self, branch_model: BranchModel) -> Branch:
    #     project = self._get_entity(branch_model.project)
    #     return Branch(
    #         name = branch_model.name,
    #         project = project,
    #         is_default = branch_model.is_default,
    #         is_protected = branch_model.is_protected,
    #         developers_can_push = branch_model.developers_can_push,
    #         developers_can_merge = branch_model.developers_can_merge,
    #         can_push = branch_model.can_push,
    #     )
        