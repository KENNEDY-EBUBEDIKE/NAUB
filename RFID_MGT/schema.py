import students.schema
import users.schema
import graphene


#  Creating the queries
class Query(students.schema.Query,
            users.schema.Query,

            graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
