from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.apps import apps
import json
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from students.serializers import StudentProfileSerializer
from staff.serializers import StaffProfileSerializer
import re

code_base_model = apps.get_model('users', 'CodeBase')
courses_model = apps.get_model('students', 'Course')
students_profile_model = apps.get_model('students', "StudentProfile")
staff_profile_model = apps.get_model('staff', 'StaffProfile')

students_scan_history_model = apps.get_model('students', "ScanRecords")
staff_scan_history_model = apps.get_model('staff', 'ScanRecords')


@api_view(["GET", "POST"])
def scan_profile(request):
    if request.method == "POST":
        rfid_code = request.POST.get('rfid_code').strip()
        rfid_code = re.sub(r'[\x00-\x1F]+', '', rfid_code)
        response = status_checker(rfid_code=rfid_code)
        if response['status'] == "STUDENT":
            student = response['student']
            update_last_scan(person=student)
            ser_student = StudentProfileSerializer(student)
            return Response(
                    {
                        "success": True,
                        "is_staff": False,
                        "student": ser_student.data,
                    })

        # For Staff *********************************************************************************

        elif response['status'] == "STAFF":
            staff = response['staff']
            update_last_scan(person=staff)
            ser_staff = StaffProfileSerializer(staff)
            return Response(
                {
                    "success": True,
                    "is_staff": True,
                    "staff": ser_staff.data
                }
            )

        # Card Does not Exist ***********************************************************************

        elif not response['status']:
            return Response(
                {
                    "success": False,
                    "message": "CARD DOES NOT EXIST"
                }
            )

    return render(request, "scan_profile.html")


def update_r(person=None, new_rfid_code=None):
    try:
        existing = code_base_model.objects.get(rfid_code=new_rfid_code)
        return existing

    except ObjectDoesNotExist:
        if person.rfid_code is None:
            new_codebase = code_base_model(owner=person, rfid_code=new_rfid_code)
            new_codebase.save()
        else:
            try:
                existing = code_base_model.objects.get(rfid_code=person.rfid_code)
                existing.rfid_code = new_rfid_code
                existing.save()
            except ObjectDoesNotExist:
                new_codebase = code_base_model(owner=person, rfid_code=new_rfid_code)
                new_codebase.save()
        person.rfid_code = new_rfid_code
        person.save()
        return "SUCCESS"


def update_last_scan(person):
    person.last_scan = datetime.now(tz=timezone.get_default_timezone())
    person.save()

    try:
        assert (type(person) is students_profile_model)
        new_record = students_scan_history_model()
        new_record.student = person
        new_record.scan_time = datetime.now(tz=timezone.get_default_timezone())
        new_record.save()
    except AssertionError:
        new_record = staff_scan_history_model()
        new_record.staff = person
        new_record.scan_time = datetime.now(tz=timezone.get_default_timezone())
        new_record.save()


def status_checker(rfid_code):

    try:
        obj = code_base_model.objects.get(rfid_code=rfid_code)
        try:
            assert (type(obj.owner) is students_profile_model)
            print("This is student")
            return {"student": obj.owner, 'status': 'STUDENT'}
        except AssertionError:
            print("This is Staff")
        return {"staff": obj.owner, 'status': 'STAFF'}
    except ObjectDoesNotExist:
        print("Card Does Not Exist")
        return {'status': None}


def db_to_ui_user_privilege(privilege):
    if privilege == 1:
        privilege = "FIRST CLASS"
    elif privilege == 2:
        privilege = "SECOND CLASS"
    elif privilege == 3:
        privilege = "THIRD CLASS"
    elif privilege == 4:
        privilege = "FOURTH CLASS"
    elif privilege == 5:
        privilege = "FIFTH CLASS"
    return privilege


def ui_to_db_user_privilege(privilege):
    if privilege == "FIRST CLASS":
        privilege = 1
    elif privilege == "SECOND CLASS":
        privilege = 2
    elif privilege == "THIRD CLASS":
        privilege = 3
    elif privilege == "FOURTH CLASS":
        privilege = 4
    elif privilege == "FIFTH CLASS":
        privilege = 5
    return privilege


def search_profile(request):
    if request.method == "POST":
        id_number = request.POST.get('id_number').upper()
        try:
            staff = staff_profile_model.objects.get(staff_id_number=id_number)
            return HttpResponse(
                content=json.dumps(
                    {
                        "is_staff": True,
                        "staff": json.loads(serializers.serialize('json', [staff, ])),
                        "status_code": 1
                    }
                ),
                content_type='application/json')
        except ObjectDoesNotExist:
            try:
                student = students_profile_model.objects.get(matric_number=id_number)
                return HttpResponse(
                    content=json.dumps(
                        {
                            "is_staff": False,
                            "student": json.loads(serializers.serialize('json', [student, ])),
                            "status_code": 1
                        }
                    ),
                    content_type='application/json')
            except ObjectDoesNotExist:
                return HttpResponse(
                    content=json.dumps(
                        {
                            "status_code": 0
                        }
                    ),
                    content_type='application/json')
