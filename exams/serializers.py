from rest_framework import serializers
from .models import AttendanceSheet, InvigilatorAttendanceSheet
from students.serializers import StudentProfileSerializer, CourseSerializer


class AttendanceSheetSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = AttendanceSheet
        fields = "__all__"


class InvigilatorAttendanceSheetSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = InvigilatorAttendanceSheet
        fields = "__all__"
