from git_api.commons.dependencies import Dependencies


if __name__ == "__main__":
    dependencies = Dependencies()
    db_provider = dependencies.database_provider
    db_provider.set_up_db()

    for project in dependencies.repo_entities.get_projects_all():
        # if project.name == "Entrées de commande":
        dependencies.api_provider.modify_branch_protection(
            project.gitlab_id,
            project.default_branch,
            push_access_level="0",
            merge_access_level="30",
        )
        print(f"{project.name} protected")

    ########
    # Test de update_all
    ########

    # from pathlib import Path
    # db_path = (
    #   Path.home() / "AppData" / "Roaming" / "By_DB" / "Git Api" / "git_api.gadb"
    # )
    # db_provider.save_as(db_path)
    # db_updater = dependencies.database_updater
    # db_updater.update_all()

    #####
    # Test sur des membres et les commits par membres
    #####

    # from git_api.database.peewee.models import CommitModel, MemberModel
    #
    # members = MemberModel().select()
    # member_names = [str(member.name).lower() for member in members]
    # print(member_names)
    # names_without_member = set()
    # names_with_multiple_members = set()
    # for commit_model in CommitModel.select():
    #     names = [
    #         name
    #         for name in member_names
    #         if str(commit_model.author_name).lower() == name
    #     ]
    #     if len(names) == 0:
    #         names_without_member.add(commit_model.author_name)
    #     elif (len(names)) >= 2:
    #         names_with_multiple_members.add(commit_model.author_name)
    #
    # print("0 correspondances")
    # for name in names_without_member:
    #     print(name)
    # print("\nmultiple correspondances")
    # for name in names_with_multiple_members:
    #     print(name)
