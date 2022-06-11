from django.core import serializers
from django.shortcuts import render, redirect, resolve_url, HttpResponse
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from .forms import StudentRegistrationForm, StudentProfileUpdateForm, CourseAddForm
from django.urls import reverse
from django.conf import settings
from RFID_MGT import utils
import csv
import io
import xlsxwriter
import os
import re
from rest_framework.response import Response
from .serializers import StudentProfileSerializer
from rest_framework.decorators import api_view

# from django.core.cache import cache

# from django.core import serializers
import json
# from django.forms.models import model_to_dict

code_base_model = apps.get_model('users', 'CodeBase')
courses_model = apps.get_model('students', 'Course')
students_profile_model = apps.get_model('students', "StudentProfile")
staff_profile_model = apps.get_model('staff', 'StaffProfile')


@login_required()
def register_student(request):
    if request.user.privilege <= 3:
        course = courses_model.objects.all()

        empty_form = StudentRegistrationForm()
        if request.method == "POST":
            form = StudentRegistrationForm(request.POST, request.FILES)
            if form.is_valid():

                new_student = students_profile_model()
                new_student.surname = form.cleaned_data['surname'].upper()
                new_student.first_name = form.cleaned_data['first_name'].upper()
                new_student.other_name = form.cleaned_data['other_name'].upper()

                new_student.email = form.cleaned_data['email'].lower()
                new_student.phone_number = form.cleaned_data['phone_number']

                new_student.matric_number = form.cleaned_data['matric_number'].upper()
                new_student.faculty = form.cleaned_data['faculty'].upper()
                new_student.department = form.cleaned_data['department'].upper()
                new_student.level = form.cleaned_data['level'].upper()
                new_student.session = form.cleaned_data['session']

                new_student.gender = form.cleaned_data['gender'].upper()
                new_student.date_of_birth = form.cleaned_data['date_of_birth']
                new_student.nationality = form.cleaned_data['nationality'].upper()
                new_student.state_of_origin = form.cleaned_data['state_of_origin'].upper()
                new_student.lga = form.cleaned_data['lga'].upper()
                new_student.resident_address = form.cleaned_data['resident_address'].lower()
                new_student.photo = form.cleaned_data['photo']
                new_student.save()

                course_offered = (request.POST.getlist("course"))

                for c in course_offered:
                    cc = courses_model.objects.get(course_code=c)
                    new_student.courses.add(cc)
                new_student.save()
                return render(request, 'student_registration.html', {"response": "SUCCESSFUL",
                                                                     "courses": course,
                                                                     "form": empty_form})
            else:
                pass

        return render(request, 'student_registration.html', {"courses": course, "form": empty_form})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def student_database(request):

    if request.user.privilege <= 3:
        all_students = students_profile_model.objects.all()
        if request.method == 'POST':
            if request.POST.get('export'):
                fac = request.POST.get('fac')
                lev = request.POST.get('lev')
                if fac or lev:
                    if fac and lev:
                        all_students = students_profile_model.objects.filter(faculty=fac, level=lev)
                        response = students_database_to_xlxs(data=all_students)
                        return response
                    elif fac:
                        all_students = students_profile_model.objects.filter(faculty=fac)
                        response = students_database_to_xlxs(data=all_students)
                        return response
                    elif lev:
                        all_students = students_profile_model.objects.filter(level=lev)
                        response = students_database_to_xlxs(data=all_students)
                        return response
                else:
                    response = students_database_to_xlxs(data=all_students)
                    return response
            else:
                faculty = request.POST.get('faculty')
                level = request.POST.get('level')

                if faculty and level:
                    all_students = students_profile_model.objects.filter(faculty=faculty, level=level)
                    return render(request, 'students_database.html', {
                        "all_students": all_students,
                        "fac": faculty,
                        "lev": level})
                elif faculty:
                    all_students = students_profile_model.objects.filter(faculty=faculty)
                    return render(request, 'students_database.html', {"all_students": all_students, "fac": faculty})
                elif level:
                    all_students = students_profile_model.objects.filter(level=level)
                    return render(request, 'students_database.html', {"all_students": all_students, "lev": level})
        else:
            return render(request, 'students_database.html', {"all_students": all_students})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def student_full_profile(request, student_id):
    if request.user.privilege <= 3:
        student = students_profile_model.objects.get(id=student_id)
        offering = student.courses.all()
        all_courses = courses_model.objects.all()
        scan_history = student.scan_records.all()
        return render(request, 'student_full_profile2.html',
                      {'student': student,
                       'offering': offering,
                       'all_courses': all_courses,
                       'scan_history': scan_history})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def flag_student(request, student_id):
    if request.user.privilege <= 2:
        student = students_profile_model.objects.get(id=student_id)
        if request.method == "POST":
            if request.POST.get("reason") == 'OTHER':
                reason = request.POST.get("other_reason")
            else:
                reason = request.POST.get("reason")
            student.is_flaged = reason
            student.save()
            return redirect(f'/students/student-profile/{student.id}')
        else:
            student.is_flaged = None
            student.save()
            return redirect(f'/students/student-profile/{student.id}')
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def student_profile_update(request, student_id):
    if request.user.privilege <= 3:
        course = courses_model.objects.all()

        student = students_profile_model.objects.get(id=student_id)

        initial_data = {}
        #  getting the initial data fields and values
        for f in StudentProfileUpdateForm().fields:
            value = getattr(student, f)
            initial_data.update({f: value})  # Save them to the initial data dictionary.

        template = 'student_profile_update_form.html'
        old_form = StudentProfileUpdateForm(initial=initial_data)

        if request.method == 'POST':
            form = StudentProfileUpdateForm(request.POST, request.FILES)  # feed the Post data to the form
            if form.is_valid():  # validate the form
                for field in form.changed_data:  # looping through the fields that did not return empty
                    setattr(student, field, form.cleaned_data[field])  # set the model field to the new data
                student.save()

                course_offered = (request.POST.getlist("course"))
                if course_offered:
                    for i in student.courses.all():
                        student.courses.remove(i)
                    for c in course_offered:
                        cc = courses_model.objects.get(course_code=c)
                        student.courses.add(cc)
                    student.save()
                else:
                    pass
                return redirect(f'/students/student-profile/{student.id}')
            else:
                return render(request, template_name=template, context={'form': old_form,
                                                                        'errors': form.errors,
                                                                        "courses": course})

        return render(request, template_name=template, context={"courses": course, 'form': old_form})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def student_profile_deactivate(request, student_id):
    if request.user.privilege <= 2:
        student = students_profile_model.objects.get(id=student_id)
        if student.is_active:
            student.is_active = False

            if student.rfid_code:
                try:
                    code_base_model.objects.get(rfid_code=student.rfid_code).delete()
                except ObjectDoesNotExist:
                    pass
                student.rfid_code = None
        else:
            student.is_active = True
        student.save()
        return redirect('/students/student-database')
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


def error(request):
    return render(request, 'error2.html')


@login_required()
def add_course(request):
    if request.user.privilege <= 3:
        empty_form = CourseAddForm()
        if request.method == "POST":
            form = CourseAddForm(request.POST)
            if form.is_valid():
                new_course = courses_model()

                new_course.course_code = form.cleaned_data['course_code'].upper()
                new_course.course_title = form.cleaned_data['course_title'].upper()
                new_course.course_faculty = form.cleaned_data['course_faculty'].upper()
                new_course.course_department = form.cleaned_data['course_department'].upper()
                new_course.credit_unit = form.cleaned_data['credit_unit']
                new_course.save()

                return render(request, 'add_course.html', {"response": "SUCCESSFUL", "form": empty_form})

        return render(request, 'add_course.html', {"form": empty_form})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def delete_course(request, course_id):
    if request.user.privilege <= 2:
        course = courses_model.objects.get(id=course_id)
        course.delete()
        return redirect('/students/courses-database')
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def courses_database(request):
    if request.user.privilege <= 3:
        courses = courses_model.objects.all()
        # courses = serializers.serialize('json', [courses, ])  # serialises(converts) model obj(to json obj) and dumps
        # data = {'success': True, 'data': json.loads(courses)}
        # return HttpResponse(json.dumps(data), content_type='application/json')
        return render(request, 'courses_database.html', {"courses": courses})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required(login_url='/users/login')
def students_data_upload(request):
    if request.user.privilege <= 3:
        if request.method == 'POST':
            csv_file = request.FILES.get('data')  # getting the file content of the POST

            if csv_file is None:
                return redirect(reverse('students_data_upload'))

            if csv_file.name.endswith('.csv'):  # Ensuring that the uploaded file is in csv format

                decoded_file = csv_file.read().decode('UTF-8')  # Reading and decoding the file.
                converted_file = io.StringIO(decoded_file)  # converting the file to a string so it can be iterated.

                # Return the next item from the iterator. so that first item(header) in the file is skipped.
                next(converted_file)

                duplicates = []
                for field in csv.reader(converted_file, delimiter=',', quotechar="'"):
                    # looping through the columns....
                    # delimiter indicates that the columns are separated by commas
                    # quote-char indicates the character for escaping any quote in the file
                    try:
                        students_profile_model.objects.create(

                            matric_number=field[0],

                            surname=field[1],
                            first_name=field[2],
                            other_name=field[3],

                            phone_number=field[4],
                            email=field[5],

                            faculty=field[6],
                            department=field[7],
                            session=field[8],
                            level=field[9],
                            gender=field[10],
                            date_of_birth=field[11],
                            nationality=field[12],
                            state_of_origin=field[13],
                            lga=field[14]
                        )
                    except IntegrityError:
                        duplicates.append(f'There is duplicate issue with {field[0]}')
                        continue
                return render(request, 'students_data_upload.html', {
                    'message': 'Data Uploaded Successfully',
                    'duplicates': duplicates})
            else:
                return render(request, 'students_data_upload.html', {'error': 'File Must be a CSV file'})
        else:
            return render(request, 'students_data_upload.html')
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


def students_database_to_xlxs(data=None):
    # Create an new Excel file and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

#  Add formats to workbook.
    bold = workbook.add_format({'bold': True, 'align': 'center'})
    merge_format = workbook.add_format({'bold': True,
                                        'border': 6,
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'fg_color': '#ffff'})


#  Merging cells
    worksheet.merge_range('C11:C12', 'NIGERIA ARMY UNIVERSITY BIU',
                          merge_format)
    worksheet.write('C13', 'COMPREHENSIVE LIST', bold)

# Inserting an image inside the worksheet.
    img = worksheet.insert_image('C1', os.path.join(os.getcwd(), 'static/scan_profile/img/naub.png'),
                                 {'x_offset': 55,
                                  'y_offset': 10,
                                  'x_scale': 0.6,
                                  'y_scale': 0.6})
    worksheet.merge_range('C1:C10', img)

    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 40)
    worksheet.set_column('E:E', 20)

    # writing to the sheet.
    worksheet.write('A15', 'Matric Number', bold)
    worksheet.write('B15', 'Name', bold)
    worksheet.write('C15', 'FACULTY', bold)
    worksheet.write('D15', 'DEPARTMENT', bold)
    worksheet.write('E15', 'Level', bold)

    row = 15
    for student in data:
        worksheet.write(row, 0, student.matric_number)
        worksheet.write(row, 1, student.surname + "    " + student.first_name)
        worksheet.write(row, 2, student.faculty)
        worksheet.write(row, 3, student.department)
        worksheet.write(row, 4, student.level)
        row += 1

    # add table to worksheet
    worksheet.add_table(14, 0, 14 + len(data), 4)

    workbook.close()

    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = f'attachment;filename="Students".xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response


# def testing_cache(request):
#     if request.method == "POST":
#         full_name = request.POST.get('full_name')
#         print(full_name)
#         amount = request.POST.get('amount')
#
#         # old = cache.get('amount1', 'Does Not Exist')
#         # print(old)
#         # updated = old + amount
#         # cache.set('data4', {"amount": amount, "full_name": full_name}, 1000)
#         # cache.set('data3', 'EVERLASTING', 1000)
#         # cache.set('data2', ["ABUJA", "LAGOS", 'BENIN'], 1000)
#         print(cache.get('*'))
#         total_amount = cache.get('data2', 'Does Not Exist')
#
#         data = {"total_amount": total_amount}
#         return render(request, 'testing_cache.html', data)
#     return render(request, 'testing_cache.html')


def register_course(request, student_id):
    all_courses = courses_model.objects.all()
    student = students_profile_model.objects.get(id=student_id)

    if request.method == "POST":
        course_offered = request.POST.getlist("course_offered[]")
        print(course_offered)

        if course_offered:
            for i in student.courses.all():
                student.courses.remove(i)
            for c in course_offered:
                cc = courses_model.objects.get(course_code=c)
                student.courses.add(cc)
            student.save()
            return HttpResponse(content=json.dumps(
                    {
                        "success": "success"
                    }
                ),
                content_type='application/json')

    return render(
        request,
        'register_course.html',
        {"all_courses": all_courses, "offering": student.courses.all(), "pk": student.pk}
    )


def student_lecture_attendance(request):
    if request.method == "POST":
        student_rfid_code = request.POST.get('rfid_code')
        course_code = request.POST.get('course_code')
        student_rfid_code = re.sub(r'[\x00-\x1F]+', '', student_rfid_code)
        response = utils.status_checker(rfid_code=student_rfid_code)
        try:
            course = courses_model.objects.get(course_code=course_code)
        except ObjectDoesNotExist:
            return HttpResponse(
                content=json.dumps(
                    {
                        "status_code": 0,
                    }
                ),
                content_type='application/json')
        if response['status'] == "STUDENT":
            student = response['student']
            utils.update_last_scan(person=student)
            print(f"This student is offering {student.courses.all()}")
            print(f"{course} is offered by {course.StudentProfile.all().count()} students")
            if course in student.courses.all():
                return HttpResponse(
                    content=json.dumps(
                        {
                            "student": json.loads(serializers.serialize('json', [student, ])),
                            "number_of_students": course.StudentProfile.all().count(),
                            "status_code": 1,
                        }
                    ),
                    content_type='application/json')
            else:
                return HttpResponse(
                    content=json.dumps(
                        {
                            "status_code": 2,
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


@api_view(["GET"])
# @permission_classes(permissions.AllowAny)
def api_test(request):
    all_students = students_profile_model.objects.all()
    student_serializer = StudentProfileSerializer(all_students, many=True)
    return Response({"success": True, "students": student_serializer.data})


@login_required()
def update_rfid_code(request, student_id):
    if request.user.privilege <= 2:
        if request.method == "POST":
            new_rfid_code = request.POST.get('code').strip()
            if len(new_rfid_code) > 1:
                rfid_code = re.sub(r'[\x00-\x1F]+', '', new_rfid_code)
                student = students_profile_model.objects.get(id=student_id)
                if student.is_active:
                    response = utils.update_r(person=student, new_rfid_code=rfid_code)
                    if response != 'SUCCESS':
                        return HttpResponse(content=json.dumps({
                            'status': 'EXISTING',
                            'rfid_code': response.rfid_code,
                            'first_name': response.owner.first_name,
                            'surname': response.owner.surname,

                        }), content_type='application/json')
                    else:
                        return HttpResponse(content=json.dumps({
                            'status': 'SUCCESS',
                            'rfid_code': students_profile_model.objects.get(id=student_id).rfid_code,
                        }), content_type='application/json')
                else:
                    return HttpResponse(content=json.dumps({
                        'status': 'NOT ACTIVE',
                    }), content_type='application/json')
            else:
                pass
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
