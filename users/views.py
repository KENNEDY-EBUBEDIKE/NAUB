from django.core import serializers
from django.shortcuts import render, resolve_url, redirect, HttpResponse
from .models import User
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.conf import settings
from django.http import HttpResponseRedirect
# from django.core.exceptions import ObjectDoesNotExist
# from django.db.utils import IntegrityError
from django.apps import apps
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.views import logout_then_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from RFID_MGT import utils
import re
admin_model = apps.get_model("users", "User")

redirect_field_name = REDIRECT_FIELD_NAME


def csrf_failure(request, reason=""):
    if settings.DEBUG:
        ctx = {'csrf_failure': reason}
        return render(request, 'login.html', ctx)
    else:
        logout_then_login(request)


def get_redirect_url(request):
    """Return the user-originating redirect URL if it's safe."""
    redirect_to = request.POST.get(
        redirect_field_name,
        request.GET.get(redirect_field_name, '')
    )

    url_is_safe = url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    )
    return redirect_to if url_is_safe else ''


def login_view(request):
    if request.method == 'POST':
        # aa = User.objects.get(email='abubakarpindar@gmail.com')
        # aa.backend = 'django.contrib.auth.backends.ModelBackend'
        # login(request, aa)
        # return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                next_url = get_redirect_url(request)
                if user.is_staff:
                    return HttpResponseRedirect(next_url or resolve_url(settings.LOGIN_REDIRECT_URL))
                else:
                    return HttpResponseRedirect(resolve_url(settings.LOGOUT_URL))
            else:
                return render(request, 'login.html', {"error_message": "Incorrect Password"})  # incorrect password
        else:
            return render(request, 'login.html', {"error_message": "User does not Exist"})  # user does not exist
    return render(request, 'login.html')


@login_required()
def admin_dashboard(request):
    if request.user.is_authenticated:

        return render(request, "dashboard.html")
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def admin_database(request):
    if request.user.privilege == 1:
        all_admins = admin_model.objects.all()
        return render(request, 'admin_database.html', {"all_admins": all_admins})
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def deactivate_admin(request, admin_id):
    if request.user.privilege == 1:
        admin = admin_model.objects.get(id=admin_id)
        if admin.is_active:
            admin.is_staff = False
            admin.is_active = False
            admin.profile.is_admin = False

        else:
            if admin.profile.is_active:
                admin.is_staff = True
                admin.is_active = True
                admin.profile.is_admin = True
            else:
                pass
        admin.profile.save()
        admin.save()

        return redirect(reverse("admin_database"))
    else:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required()
def change_privilege(request):
    if request.user.privilege == 1:
        if request.method == "POST":
            command = request.POST.get('command')
            admin = admin_model.objects.get(id=request.POST.get('admin_id'))
            if command == "increase":
                if admin.privilege > 1:
                    admin.privilege -= 1
            elif command == "decrease":
                if admin.privilege < 5:
                    admin.privilege += 1
            admin.save()
            return HttpResponse(
                json.dumps(
                    {
                        "success": True,
                        "privilege": utils.db_to_ui_user_privilege(admin.privilege)
                    }),
                content_type='application/json')
    else:
        return HttpResponse(
            json.dumps({"error": "You Dont Have Required Privilege"}),
            content_type='application/json')


def login_on_scan(request):
    if request.method == "POST":
        rfid_code = request.POST.get('rfid_code')
        rfid_code = re.sub(r'[\x00-\x1F]+', '', rfid_code)
        response = utils.status_checker(rfid_code=rfid_code)
        if response['status'] == "STAFF":

            staff = response['staff']
            if staff.is_admin:
                usr = staff.user
                ser_usr = serializers.serialize('json', [usr, ])
                ser_staff = serializers.serialize('json', [staff, ])
                utils.update_last_scan(person=staff)
                return HttpResponse(
                    content=json.dumps(
                        {
                            "staff": json.loads(ser_staff),
                            "user": json.loads(ser_usr),
                            "status_code": 1,
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
        else:
            return HttpResponse(
                content=json.dumps(
                    {
                        "status_code": 0,
                    }
                ),
                content_type='application/json')
