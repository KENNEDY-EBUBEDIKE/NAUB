from django.shortcuts import render, redirect, reverse, resolve_url
from django.contrib.auth.decorators import login_required
from .forms import StaffRegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.apps import apps
from datetime import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import IntegrityError
from RFID_MGT import utils
from django.conf import settings
from django.http import HttpResponse
import json
import re


user_model = get_user_model()
staff_profile_model = apps.get_model('staff', 'StaffProfile')
staff_work_attendance_model = apps.get_model('staff', 'StaffWorkAttendance')
code_base_model = apps.get_model('users', "CodeBase")


@login_required()
def register_staff(request):
    if request.user.privilege <= 2:
        empty_form = StaffRegistrationForm()
        if request.method == "POST":
            form = StaffRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                new_staff = staff_profile_model()

                #  Creating Staff
                new_staff.save()
                new_staff.surname = form.cleaned_data['surname'].upper()
                new_staff.first_name = form.cleaned_data['first_name'].upper()
                new_staff.other_name = form.cleaned_data['other_name'].upper()

                new_staff.staff_id_number = form.cleaned_data['staff_id_number'].upper()
                new_staff.gender = form.cleaned_data['gender'].upper()
                new_staff.date_of_birth = form.cleaned_data['date_of_birth']

                new_staff.lga = form.cleaned_data['lga'].upper()
                new_staff.nationality = form.cleaned_data['nationality'].upper()
                new_staff.state_of_origin = form.cleaned_data['state_of_origin'].upper()

                new_staff.photo = request.FILES.get("photo")

                new_staff.department = form.cleaned_data['department'].upper()
                new_staff.designation = form.cleaned_data['designation'].upper()

                new_staff.phone_number = form.cleaned_data['phone_number']
                new_staff.email = form.cleaned_data['email']

                new_staff.save()

                return render(request, 'staff_registration.html', {'form': empty_form, "response": "SUCCESSFUL"})
        return render(request, 'staff_registration.html', {'form': empty_form})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def staff_profile_update(request, staff_id):
    if request.user.privilege <= 2:
        staff = staff_profile_model.objects.get(id=staff_id)

        initial_data = {}
        #  getting the initial data fields and values
        for f in StaffRegistrationForm().fields:
            value = getattr(staff, f)
            initial_data.update({f: value})  # Save them to the initial data dictionary.

        template = 'staff_profile_update_form.html'
        old_form = StaffRegistrationForm(initial=initial_data)

        if request.method == 'POST':
            form = StaffRegistrationForm(request.POST, request.FILES)  # feed the Post data to the form
            if form.is_valid():  # validate the form
                for field in form.changed_data:  # looping through the fields that did not return empty
                    setattr(staff, field, form.cleaned_data[field])  # set the model field to the new data
                staff.save()
                return redirect(reverse("staff_full_profile", kwargs={"staff_id": staff.pk}))
            else:
                print("there are errors")
                print(form.errors)
                return render(request, template_name=template, context={'form': old_form, 'errors': form.errors})
        return render(request, template_name=template, context={'form': old_form})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def make_admin(request):
    if request.user.privilege == 1:
        if request.method == "POST":
            staff = staff_profile_model.objects.get(id=request.POST.get('staff_id'))

            email = staff.email
            username = request.POST.get('username').upper()
            password = request.POST.get('password')
            privilege = request.POST.get('privilege').upper()

            #  ***********************************************************************************************************
            try:
                if privilege == "FIRST CLASS":
                    new_admin = user_model.objects.create_superuser(username=username, email=email, password=password)
                else:
                    new_admin = user_model.objects.create_user(username=username, email=email, password=password)
                staff.is_admin = True
                staff.save()
            except IntegrityError as e:
                return render(request, 'staff_full_profile.html', {'staff': staff, 'error': e})

            new_admin.profile = staff
            new_admin.privilege = utils.ui_to_db_user_privilege(privilege)
            new_admin.save()
        return redirect("/users/admin-database")
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def staff_full_profile(request, staff_id):
    if request.user.privilege <= 2:
        staff = staff_profile_model.objects.get(id=staff_id)
        scan_history = staff.scan_records.all()
        if staff.is_admin:
            privilege = utils.db_to_ui_user_privilege(staff.user.privilege)
            return render(request, 'staff_full_profile.html', {'staff': staff,
                                                               'privilege': privilege,
                                                               'scan_history': scan_history})
        else:
            return render(request, 'staff_full_profile.html', {'staff': staff, 'scan_history': scan_history})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def flag_staff(request, staff_id):
    if request.user.privilege <= 2:
        staff = staff_profile_model.objects.get(id=staff_id)
        if request.method == "POST":
            if request.POST.get("reason") == 'OTHER':
                reason = request.POST.get("other_reason")
            else:
                reason = request.POST.get("reason")
            staff.is_flaged = reason
            staff.save()
            return redirect(f'/staff/staff-profile/{staff.id}')
        else:
            staff.is_flaged = None
            staff.save()
            return redirect(f'/staff/staff-profile/{staff.id}')
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def staff_database(request):
    if request.user.privilege <= 2:
        all_staff = staff_profile_model.objects.all()
        return render(request, 'staff_database.html', {"all_staff": all_staff})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def deactivate_staff(request, staff_id):
    if request.user.privilege == 1:
        staff = staff_profile_model.objects.get(id=staff_id)

        if staff.is_active:
            staff.is_active = False

            if staff.rfid_code:
                try:
                    code_base_model.objects.get(rfid_code=staff.rfid_code).delete()
                except ObjectDoesNotExist:
                    pass
                staff.rfid_code = None

            if staff.is_admin:
                staff.user.is_active = False
                staff.user.is_staff = False
            else:
                pass
        else:
            staff.is_active = True
            if staff.is_admin:
                staff.user.is_active = True
                staff.user.is_staff = True
            else:
                pass
        staff.user.save()
        staff.save()

        return redirect(reverse("staff_database"))
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@csrf_exempt
def work_attendance_scan(request):
    if request.method == "POST":
        rfid_code = request.POST.get('rfid_code')
        rfid_code = re.sub(r'[\x00-\x1F]+', '', rfid_code)
        try:
            staff = staff_profile_model.objects.get(rfid_code=rfid_code)
            utils.update_last_scan(person=staff)
            try:
                attendance = staff_work_attendance_model.objects.get(
                    staff=staff,
                    sign_in_time__date=datetime.date(
                        datetime.now(tz=timezone.get_default_timezone())
                    )
                )
                if not attendance.sign_out_time:
                    attendance.sign_out_time = datetime.now(tz=timezone.get_default_timezone())
                    attendance.save()

                    return JsonResponse({"status": 'STAFF SIGNED OUT'}, safe=False)
                else:
                    return JsonResponse({"status": 'STAFF ALREADY SIGNED OUT'}, safe=False)

            except ObjectDoesNotExist:
                new_work_attendance = staff_work_attendance_model()

                new_work_attendance.staff = staff
                new_work_attendance.sign_in_time = datetime.now(tz=timezone.get_default_timezone())
                new_work_attendance.save()
                return JsonResponse({"status": 'STAFF SIGNED IN'}, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({"status": 'STAFF DOES NOT EXIST'}, safe=False)
    else:
        pass


@login_required()
def delete_work_attendance(request, attendance_id):
    if request.user.privilege <= 2:
        attendance = staff_work_attendance_model.objects.get(id=attendance_id)
        attendance.delete()
        return redirect(reverse("work_attendance_sheet"))
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def work_attendance_sheet(request):
    if request.user.privilege <= 2:
        all_attendance = staff_work_attendance_model.objects.all()
        return render(request, 'staff_work_attendance_sheet.html', {'all_attendance': all_attendance})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def update_rfid_code(request, staff_id):
    if request.user.privilege <= 2:
        if request.method == "POST":
            new_rfid_code = request.POST.get('code').strip()
            if len(new_rfid_code) > 1:
                new_rfid_code = re.sub(r'[\x00-\x1F]+', '', new_rfid_code)
                staff = staff_profile_model.objects.get(id=staff_id)
                if staff.is_active:
                    response = utils.update_r(person=staff, new_rfid_code=new_rfid_code)
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
                            'rfid_code': staff_profile_model.objects.get(id=staff_id).rfid_code,
                        }), content_type='application/json')
                else:
                    return HttpResponse(content=json.dumps({
                        'status': 'NOT ACTIVE',
                    }), content_type='application/json')
            else:
                pass
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


def confirm_staff_status(request):
    if request.method == "POST":
        staff_rfid_code = request.POST.get('rfid_code')
        staff_rfid_code = re.sub(r'[\x00-\x1F]+', '', staff_rfid_code)
        response = utils.status_checker(rfid_code=staff_rfid_code)
        if response['status'] == "STAFF":
            staff = response['staff']
            utils.update_last_scan(person=staff)
            return HttpResponse(
                content=json.dumps(
                    {
                        "status_code": 1,
                        "staff_name": f'{staff.first_name} {staff.surname}',
                        "staff_id_number": staff.staff_id_number,
                        "staff_designation": staff.designation,
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
