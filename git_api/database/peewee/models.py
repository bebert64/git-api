from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    ForeignKeyField,
    DateField,
    BooleanField,
)

database = SqliteDatabase(None)


class BaseModel(Model):
    gitlab_id = CharField(primary_key=True)

    class Meta:  # pylint: disable=too-few-public-methods
        database = database


class GroupModel(BaseModel):
    name = CharField()
    web_url = CharField()
    description = CharField()
    project_creation_level = CharField()
    parent = ForeignKeyField("self", backref="children", null=True)


class MemberModel(BaseModel):
    username = CharField()
    name = CharField()
    role = CharField()


class ProjectModel(BaseModel):
    name = CharField()
    description = CharField(null=True)
    web_url = CharField()
    default_branch = CharField(null=True)
    topics = CharField()
    group = ForeignKeyField(GroupModel)


class BranchModel(BaseModel):

    name = CharField()
    project = ForeignKeyField(ProjectModel)
    is_default = BooleanField()
    is_protected = BooleanField()
    developers_can_push = BooleanField()
    developers_can_merge = BooleanField()
    can_push = BooleanField()


class CommitModel(BaseModel):

    title = CharField()
    author_name = CharField()
    author_email = CharField()
    committed_date = DateField()
    message = CharField()
    web_url = CharField()
    branch = ForeignKeyField(BranchModel)
    member = ForeignKeyField(MemberModel, null=True)


class TagModel(BaseModel):
    commit = ForeignKeyField(CommitModel)
    name = CharField()
    message = CharField()
