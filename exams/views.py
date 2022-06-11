from django.shortcuts import render, redirect, reverse, resolve_url
from django.http import JsonResponse, HttpResponse
from django.apps import apps
from django.conf import settings
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import pytz
from RFID_MGT import utils
import xlsxwriter
import io
import re
import time

import json
from django.core import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from students.serializers import StudentProfileSerializer, CourseSerializer
from staff.serializers import StaffProfileSerializer
from .serializers import AttendanceSheetSerializer, InvigilatorAttendanceSheetSerializer


exam_request_model = apps.get_model('exams', "ExaminationRequest")
exam_attendance_model = apps.get_model('exams', "AttendanceSheet")
invigilator_attendance_model = apps.get_model('exams', "InvigilatorAttendanceSheet")
exam_malpractice_model = apps.get_model('exams', "ExaminationMalpractice")
students_profile_model = apps.get_model('students', "StudentProfile")
staff_profile_model = apps.get_model('staff', "StaffProfile")
courses_model = apps.get_model('students', "Course")


@csrf_exempt
@api_view(['GET', 'POST'])
def check_course(request):
    courses = courses_model.objects.all()
    if request.method == "POST":
        course_code = request.POST.get('current_exam')
        if course_code:
            try:
                course = courses_model.objects.get(course_code=course_code.upper())
                ser_course = CourseSerializer(course)
                try:
                    exam_request = exam_request_model.objects.get(course=course)

                    if exam_request.status == "APPROVED":
                        if datetime.now(tz=timezone.get_default_timezone()) >= exam_request.approved_start_time:
                            return Response(
                                {
                                    "message": "EXAM APPROVED",
                                    "course": ser_course.data
                                }
                            )
                        else:
                            return JsonResponse(
                                {
                                    "response": f"{course_code} approved Date and Time Has not Reached"
                                 },
                                safe=False)
                    else:
                        return JsonResponse(
                            {
                                "response": f"{course_code} Has Not been Approved"
                            }, safe=False)

                except ObjectDoesNotExist:
                    return JsonResponse({"response": f"{course_code}  Has Not been Requested"}, safe=False)
            except ObjectDoesNotExist:
                return JsonResponse({"response": f"{course_code} Does Not Exist"}, safe=False)
        else:
            return JsonResponse({"response": "Please Select a Course Code"}, safe=False)
    else:
        return render(request, "start-exams.html", {"courses": courses})


@api_view(["GET", "POST"])
def exam_profile(request):
    if request.method == "POST":
        current_exam = request.POST.get('current_exam').upper()
        rfid_code = request.POST.get('rfid_code')
        rfid_code = re.sub(r'[\x00-\x1F]+', '', rfid_code)
        course = courses_model.objects.get(course_code=current_exam)
        exam_request = exam_request_model.objects.get(course=course)

        response = utils.status_checker(rfid_code=rfid_code)  # checking who owns the rfid code

        # for students
        if response['status'] == "STUDENT":
            student = response['student']
            ser_student = StudentProfileSerializer(student)

            utils.update_last_scan(person=student)
            if course in student.courses.all():
                try:
                    exam_details = exam_attendance_model.objects.get(student=student, course=course)

                    if exam_details.has_written:
                        exam_detail = AttendanceSheetSerializer(exam_details)
                        return Response(
                                {
                                    "success": False,
                                    "is_staff": False,
                                    "student": ser_student.data,
                                    "exam_details": exam_detail.data,
                                    "message": "THIS STUDENT HAS ALREADY WRITTEN THIS COURSE"
                                })
                    else:  # Sign Out the student
                        time_lag = exam_details.sign_in_time + timedelta(minutes=2)
                        try:
                            assert (datetime.now(tz=timezone.get_default_timezone()) > time_lag), \
                                "DUPLICATE SCAN!, Please, Wait for two minutes before sign-out. "

                            #  ensuring students cant sign-out 1 hour after approved stop time has elapsed
                            final_time = exam_request.approved_stop_time + timedelta(hours=1)
                            if datetime.now(tz=timezone.get_default_timezone()) < final_time:
                                exam_details.has_written = True
                                exam_details.sign_out_time = time.mktime(datetime.now().timetuple())
                                # exam_details.sign_out_time = datetime.now(tz=timezone.get_default_timezone())
                                exam_details.save()

                                exam_detail = AttendanceSheetSerializer(exam_details)
                                return Response(
                                    {
                                        "success": True,
                                        "is_staff": False,
                                        "student": ser_student.data,
                                        "exam_details": exam_detail.data,
                                        "message": "STUDENT SIGNED OUT"
                                    }
                                )
                            else:
                                exam_detail = AttendanceSheetSerializer(exam_details)
                                return Response(
                                    {
                                        "success": False,
                                        "is_staff": False,
                                        "student": ser_student.data,
                                        "exam_details": exam_detail.data,
                                        "message": "STUDENT DID NOT SUBMIT ON TIME"
                                    }
                                )

                        except AssertionError:
                            exam_detail = AttendanceSheetSerializer(exam_details)
                            return Response(
                                {
                                    "success": False,
                                    "is_staff": False,
                                    "student": ser_student.data,
                                    "exam_details": exam_detail.data,
                                    "message": " Please, Wait for two minutes before sign-out. "
                                }
                            )
                except ObjectDoesNotExist:
                    #  check if exam time has passed
                    if datetime.now(tz=timezone.get_default_timezone()) <= exam_request.approved_stop_time:
                        new_attendance = exam_attendance_model()   # sign in the student
                        new_attendance.student = student
                        new_attendance.course = course
                        # new_attendance.sign_in_time = datetime.now(tz=timezone.get_default_timezone())
                        new_attendance.sign_out_time = time.mktime(datetime.now().timetuple())
                        new_attendance.save()
                        exam_details = exam_attendance_model.objects.get(student=student, course=course)
                        exam_detail = AttendanceSheetSerializer(exam_details)
                        return Response(
                            {
                                "success": True,
                                "is_staff": False,
                                "student": ser_student.data,
                                "exam_details": exam_detail.data,
                                "message": "STUDENT SIGNED IN"
                            }

                        )
                    else:
                        return Response(
                            {
                                "success": False,
                                "is_staff": False,
                                "message": "APPROVED EXAM START TIME HAS EXPIRED, "
                                           " Students Can No Longer Sign-In"
                            })
            else:
                return Response(
                    {
                        "success": False,
                        "is_staff": False,
                        "message": "This STUDENT DID NOT REGISTER FOR THIS COURSE"
                    }
                )

        # For Invigilators  *******************************************************************************************
        elif response['status'] == "STAFF":
            staff = response['staff']
            ser_staff = StaffProfileSerializer(staff)
            utils.update_last_scan(person=staff)
            invigilators = exam_request.invigilators.all()
            if staff in invigilators:   # check if the staff is an approved invigilator for the course
                try:
                    invigilator_attendance_details = invigilator_attendance_model.objects.get(invigilator=staff,
                                                                                              course=course)
                    # sign out invigilator if exam has ended
                    if datetime.now(tz=timezone.get_default_timezone()) >= exam_request.approved_stop_time:
                        if not invigilator_attendance_details.sign_out_time:
                            # invigilator_attendance_details.sign_out_time = datetime.now(
                            #     tz=timezone.get_default_timezone())
                            invigilator_attendance_details.sign_out_time = time.mktime(datetime.now().timetuple())
                            invigilator_attendance_details.save()
                        else:
                            pass
                        invigilator_attendance_detail = InvigilatorAttendanceSheetSerializer(
                            invigilator_attendance_details)
                        return Response(
                                {
                                    "success": True,
                                    "is_staff": True,
                                    "staff": ser_staff.data,
                                    "exam_details": invigilator_attendance_detail.data,
                                    "message": "INVIGILATOR SIGNED OUT"
                                })
                    else:
                        invigilator_attendance_detail = InvigilatorAttendanceSheetSerializer(
                            invigilator_attendance_details)
                        return Response(
                            {
                                "success": False,
                                "is_staff": True,
                                "staff": ser_staff.data,
                                "exam_details": invigilator_attendance_detail.data,
                                "message": "INVIGILATOR CANNOT LEAVE WHILE EXAM IS STILL IN PROGRESS"
                            }
                        )
                except Exception as e:
                    print(e)
                    # Ensuring invigilator cannot sign in 30 minutes after exam has started
                    if datetime.now(tz=timezone.get_default_timezone()) <= (
                            exam_request.approved_start_time + timedelta(minutes=5)):

                        new_invigilator_attendance = invigilator_attendance_model()
                        new_invigilator_attendance.invigilator = staff
                        new_invigilator_attendance.course = course
                        # new_invigilator_attendance.sign_in_time = datetime.now(tz=timezone.get_default_timezone())
                        new_invigilator_attendance.sign_in_time = time.mktime(datetime.now().timetuple())
                        new_invigilator_attendance.save()

                        invigilator_attendance_detail = InvigilatorAttendanceSheetSerializer(new_invigilator_attendance)
                        return Response(
                                {
                                    "success": True,
                                    "is_staff": True,
                                    "staff": ser_staff.data,
                                    "exam_details": invigilator_attendance_detail.data,
                                    "message": "INVIGILATOR SIGNED IN"
                                })
                    else:
                        return Response(
                            {
                                "success": False,
                                "is_staff": True,
                                "message": "Invigilator Arrived Late!. "
                                           "Cannot sign-in 30 minutes after exam has commenced."
                            }
                        )
            else:
                return Response(
                    {
                        "success": False,
                        "is_staff": True,
                        "message": "This Staff Is Not an Invigilator for this Course"
                    }

                )

        elif not response['status']:
            return Response(
                {
                    "success": False,
                    "message": "CARD DOES NOT EXIST"
                }
            )


@login_required()
def exam_attendance_sheet(request):
    if request.user.privilege <= 3:
        courses = courses_model.objects.all()

        if request.method == "POST":
            course_code = request.POST.get('course')
            if course_code == "None":
                course_code = None
            level = request.POST.get('level')
            if level == "None":
                level = None
            faculty = request.POST.get('faculty')
            if faculty == "None":
                faculty = None
            attendance_list = []
            if course_code:
                course = courses_model.objects.get(course_code=course_code.upper())
                students_attendance = course.exam_attendance_sheet.all()

                if faculty and level:
                    for attendee in students_attendance:
                        if attendee.student.faculty == faculty and attendee.student.level == level:
                            attendance_list.append(attendee)
                elif faculty:
                    for attendee in students_attendance:
                        if attendee.student.faculty == faculty:
                            attendance_list.append(attendee)
                elif level:
                    for attendee in students_attendance:
                        if attendee.student.level == level:
                            attendance_list.append(attendee)
                else:
                    attendance_list = students_attendance
                if request.POST.get("export"):
                    response = write_exam_attendance_to_xlsx(data=attendance_list, course=course)
                    return response
                else:
                    return render(request, 'attendance_sheet.html', {"attendance": attendance_list, "courses": courses,
                                                                     "current": course,
                                                                     "level": level,
                                                                     "faculty": faculty,
                                                                     "course_code": course_code})
            else:
                return redirect(reverse("exam_attendance_sheet"))
        else:
            return render(request, 'attendance_sheet.html', {"courses": courses})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def delete_attendance(request, attendance_id):
    if request.user.privilege <= 2:
        attendance = exam_attendance_model.objects.get(id=attendance_id)
        attendance.delete()
        return redirect(reverse("exam_attendance_sheet"))
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def request_exam(request):
    if request.user.privilege <= 3:
        course_model = apps.get_model('students', "Course")
        courses = course_model.objects.all()

        exam_requests = request.user.examination_request.all()

        if request.method == 'POST':
            try:
                course = course_model.objects.get(course_code=request.POST.get('course'))
            except ObjectDoesNotExist:
                return render(request, 'exam_request.html', {'courses': courses, 'exam_requests': exam_requests})

            if exam_request_model.objects.filter(course=course).exists():
                print('EXISTS')
                return render(request, 'exam_request.html', {'courses': courses, 'exam_requests': exam_requests})
            else:
                new_request = exam_request_model()

                new_request.course = course
                new_request.requested_by = request.user

                new_request.save()

                return redirect(reverse("request_exam"))
        else:
            return render(request, 'exam_request.html', {'courses': courses, 'exam_requests': exam_requests})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def approve_exam(request):
    if request.user.privilege <= 2:
        tz = pytz.timezone(str(timezone.get_default_timezone()))
        all_exam_requests = exam_request_model.objects.all()
        all_staff = staff_profile_model.objects.all()

        if request.method == "POST":
            start_datetime = str(request.POST.get('start_date') + " " + request.POST.get('start_time'))
            stop_datetime = str(request.POST.get('stop_date') + " " + request.POST.get('stop_time'))
            invigilators = (request.POST.getlist("invigilators"))
            try:
                stop_datetime = datetime.strptime(stop_datetime, '%Y-%m-%d %H:%M')
                start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M')
            except ValueError:
                return redirect(reverse("approve_exam"))
            exam_request = exam_request_model.objects.get(id=request.POST.get('rid'))
            exam_request.approved_start_time = tz.localize(start_datetime)  # make offset-aware and save
            exam_request.approved_stop_time = tz.localize(stop_datetime)
            exam_request.status = "APPROVED"
            exam_request.approved_by = request.user
            for invigilator in invigilators:
                print(invigilator)
                staff = staff_profile_model.objects.get(surname=invigilator)
                exam_request.invigilators.add(staff)
            exam_request.save()
            return redirect(reverse("approve_exam"))
        return render(request, 'exam_approve.html', {'exam_requests': all_exam_requests, 'all_staff': all_staff})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def decline_exam_request(request, exam_request_id):
    if request.user.privilege <= 2:
        exam_request = exam_request_model.objects.get(id=exam_request_id)
        exam_request.status = "DECLINED"
        exam_request.approved_by = request.user
        exam_request.save()
        return redirect(reverse("approve_exam"))
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def delete_exam_request(request, exam_request_id):
    if request.user.privilege <= 2:
        exam_request = exam_request_model.objects.get(id=exam_request_id)
        exam_request.delete()
        return redirect(reverse("approve_exam"))
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def examination_malpractice(request):
    if request.user.privilege <= 3:
        all_courses = courses_model.objects.all()
        all_staff = staff_profile_model.objects.all()
        all_students = students_profile_model.objects.all()

        if request.method == "POST":
            student = students_profile_model.objects.get(matric_number=request.POST.get('matric_number'))
            course = courses_model.objects.get(course_code=request.POST.get('course'))

            if exam_malpractice_model.objects.filter(student=student, course=course).exists():
                return render(request, 'exam_malpractice_form.html', {"all_courses": all_courses,
                                                                      "all_staff": all_staff,
                                                                      "all_students": all_students,
                                                                      "error": "Case Already Exists"})
            else:
                new_case = exam_malpractice_model()
                new_case.student = student
                new_case.course = course
                new_case.invigilator = staff_profile_model.objects.get(surname=request.POST.get('invigilator'))
                new_case.details = request.POST.get('details')
                new_case.exhibit = request.FILES.get('exhibit')
                new_case.save()
                return render(request, 'exam_malpractice_form.html', {"all_courses": all_courses,
                                                                      "all_staff": all_staff,
                                                                      "all_students": all_students,
                                                                      "success": "Case Logged Successfully"})

        else:

            return render(request, 'exam_malpractice_form.html', {"all_courses": all_courses,
                                                                  "all_staff": all_staff, "all_students": all_students})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def invigilators_attendance_sheet(request):
    if request.user.privilege <= 2:
        courses = courses_model.objects.all()
        if request.method == "POST":
            course_code = request.POST.get('course')
            if course_code:
                course = courses_model.objects.get(course_code=course_code.upper())
                invigilators_attendance = course.invigilator_attendance_sheet.all()
                return render(request, 'invigilator_attendance_sheet.html', {"attendance": invigilators_attendance,
                                                                             "current": course,
                                                                             "courses": courses})
            else:
                return redirect(reverse(invigilators_attendance_sheet))
        return render(request, 'invigilator_attendance_sheet.html', {"courses": courses})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@csrf_exempt
def scan_to_invigilate(request):
    if request.method == "POST":
        rfid_code = request.POST.get('rfid_code')
        rfid_code = re.sub(r'[\x00-\x1F]+', '', rfid_code)
        response = utils.status_checker(rfid_code=rfid_code)
        if response['status'] == "STAFF":
            staff = response['staff']
            utils.update_last_scan(person=staff)
            exams = staff.examination_invigilator.all()
            ser_staff = serializers.serialize('json', [staff, ])

            if exams:
                lis = []
                for exam in exams:
                    lis.append(exam.course.course_code)
                print(lis)
                exams_obj = {'courses': lis}
                # ser_courses = serializers.serialize('json', [exams_obj, ])
                return HttpResponse(
                    content=json.dumps(
                        {
                            "courses": exams_obj,
                            "invigilator": json.loads(ser_staff),
                            "status_code": 1
                        }),
                    content_type='application/json')
            else:
                return HttpResponse(
                    content=json.dumps(
                        {
                            "status_code": 0,
                        }
                    ),
                    content_type='application/json')
        else:
            return HttpResponse(
                content=json.dumps(
                    {
                        "status_code": 0,
                    }
                ),
                content_type='application/json')


def write_exam_attendance_to_xlsx(data=None, course=None):

    # Create an new Excel file and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    # Add formatting to workbook.
    bold = workbook.add_format({'bold': True})
    date_time_format = workbook.add_format({'num_format': 'mmm d yyyy hh:mm AM/PM'})

    # Text Box Properties

    text = f'Course Code::  {course.course_code}\n\n' \
           f'Course Title::  {course.course_title}\n\n' \
           f'Number Of students That Registered:: {course.StudentProfile.all().count()}\n\n' \
           f'Number Of students That Attended:: {course.exam_attendance_sheet.all().count()}\n\n'\
           f'Number Of Students On This List::  {len(data)}'
#
    options = {
        'width': 400,
        'height': 200,
        'x_offset': 0,
        'y_offset': 0,

        'font': {'color': 'white',
                 'size': 12,
                 'name': 'Arial',
                 'bold': True,
                 'italic': False,
                 },

        'align': {'vertical': 'middle',
                  'horizontal': 'left',
                  'text': 'left'
                  },

        'object_position': 3,

        'line: ': {'none': False,
                   'color': 'black',
                   'width': 5.0,
                   'dash_type': 'long_dash_dot_dot'},

        'border:': {'none': True,
                    'color': 'blue'},

        'fill': {'color': '#1c3c3c'}

    }
    worksheet.insert_textbox('C2', text, options)

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 35)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('F:G', 25)

    # writing to the sheet.
    worksheet.write('A13', 'Matric Number', bold)
    worksheet.write('B13', 'Name', bold)
    worksheet.write('C13', 'FACULTY', bold)
    worksheet.write('D13', 'DEPARTMENT', bold)
    worksheet.write('E13', 'Level', bold)
    worksheet.write('F13', 'Sign-In Time', bold)
    worksheet.write('G13', 'Sign-Out Time', bold)

    row = 13
    for attendee in data:
        worksheet.write(row, 0, attendee.student.matric_number)
        worksheet.write(row, 1, attendee.student.surname + "  " + attendee.student.first_name)
        worksheet.write(row, 2, attendee.student.faculty)
        worksheet.write(row, 3, attendee.student.department)
        worksheet.write(row, 4, attendee.student.level)
        worksheet.write(row, 5, attendee.sign_in_time, date_time_format)
        worksheet.write(row, 6, attendee.sign_out_time, date_time_format)
        row += 1

    # Insert an image.
    # worksheet.insert_image('B5', 'logo.png')

    # add table to worksheet
    worksheet.add_table(12, 0, 12 + len(data), 6)

    workbook.close()

    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = f'attachment;filename="{course.course_code}_Exam Attendance".xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response


def exam_profile_view(request):
    current_exam = request.GET.get('current_exam')
    return render(request, 'exam_profile.html', {'current_exam': current_exam})
