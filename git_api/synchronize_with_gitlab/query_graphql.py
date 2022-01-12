QUERY_GRAPHQL = """
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
    group(fullPath: {{root_group_id}}) {
        ...GroupFields
        ...MemberFields
        ...GroupsRecursive
    }
}
"""
