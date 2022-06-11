import graphene
from graphql_auth import mutations
from graphql_auth.schema import MeQuery


#  Creating the queries
class Query(MeQuery, graphene.ObjectType):
    pass


class AuthMutations(graphene.ObjectType):
    tokenAuth = mutations.ObtainJSONWebToken.Field()
    verifyToken = mutations.VerifyToken.Field()
    refreshToken = mutations.RefreshToken.Field()
    revokeToken = mutations.RevokeToken.Field()


#  Creating the Mutations
class Mutation(AuthMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)
