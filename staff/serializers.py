from rest_framework import serializers
from .models import StaffProfile, StaffWorkAttendance


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = "__all__"


class StaffWorkAttendanceSerializer(serializers.ModelSerializer):
    staff = StaffProfileSerializer(read_only=True)

    class Meta:
        model = StaffWorkAttendance
        fields = "__all__"
