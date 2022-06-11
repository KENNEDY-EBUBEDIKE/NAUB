from rest_framework import serializers
from .models import StudentProfile, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class StudentProfileSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"



