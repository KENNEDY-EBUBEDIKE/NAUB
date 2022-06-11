from django.apps import apps
import graphene
from graphene_django import DjangoObjectType
from graphql_auth.constants import Messages
from graphql_auth.exceptions import GraphQLAuthError
from django.core.exceptions import ObjectDoesNotExist


studentsprofile_model = apps.get_model('students', "StudentProfile")
staffprofile_model = apps.get_model('staff', "StaffProfile")
courses_model = apps.get_model('students', "Course")


#  Creating Schema that will connect the api queries and the models
class StudentProfileType(DjangoObjectType):
    class Meta:
        model = studentsprofile_model


class CourseType(DjangoObjectType):
    class Meta:
        model = courses_model


class StaffProfileType(DjangoObjectType):

    class Meta:
        model = staffprofile_model


#  Creating the queries
class Query(graphene.ObjectType):
    students = graphene.List(StudentProfileType)
    courses = graphene.List(CourseType)
    student = graphene.Field(StudentProfileType, matricNumber=graphene.String())
    staff = graphene.Field(StaffProfileType, staffIdNumber=graphene.String())

    def resolve_students(self, cls, info, **kwargs):
        user = info.context.user
        if user.is_authenticated:
            return studentsprofile_model.objects.all()
        else:
            return GraphQLAuthError(message=Messages.UNAUTHENTICATED)

    def resolve_courses(self, info, **kwargs):
        # user = info.context.user
        return courses_model.objects.all()

    def resolve_student(self, info, **kwargs):
        matricNumber = kwargs.get('matricNumber')
        matricNumber = matricNumber.upper()
        user = info.context.user
        if user.is_authenticated:
            if matricNumber is not None:
                try:
                    return studentsprofile_model.objects.get(matric_number=matricNumber)
                except ObjectDoesNotExist:
                    return None
            else:
                return None
        else:
            return GraphQLAuthError(message=Messages.UNAUTHENTICATED)

    def resolve_staff(self, info, **kwargs):
        staffIdNumber = kwargs.get('staffIdNumber')
        staffIdNumber = staffIdNumber.upper()
        user = info.context.user
        if user.is_authenticated:
            if staffIdNumber is not None:
                try:
                    return staffprofile_model.objects.get(staff_id_number=staffIdNumber)
                except ObjectDoesNotExist:
                    return None
            else:
                return None
        else:
            return GraphQLAuthError(message=Messages.UNAUTHENTICATED)


schema = graphene.Schema(query=Query, auto_camelcase=False)
