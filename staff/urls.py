from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import staff_database,\
    deactivate_staff,\
    register_staff,\
    work_attendance_scan,\
    work_attendance_sheet,\
    staff_full_profile,\
    make_admin,\
    update_rfid_code,\
    delete_work_attendance, staff_profile_update, flag_staff, confirm_staff_status


urlpatterns = [
    path('staff-registration/', register_staff, name='register_staff'),
    path('staff-profile-update/<int:staff_id>/', staff_profile_update, name='staff_profile_update'),
    path('staff-database/', staff_database, name='staff_database'),
    path('staff-attendance/', work_attendance_scan, name='work_attendance_scan'),
    path('staff-attendance-sheet/', work_attendance_sheet, name='work_attendance_sheet'),
    path('flag-staff/<int:staff_id>/', flag_staff, name='flag_staff'),
    path('staff-activity/<int:staff_id>/', deactivate_staff, name='deactivate_staff'),
    path('staff-profile/<int:staff_id>/', staff_full_profile, name='staff_full_profile'),
    path('make-admin/', make_admin, name='make_admin'),
    path('update-rfid-code/<int:staff_id>/', csrf_exempt(update_rfid_code), name="update_rfid_code"),
    path('delete-work-attendance/<int:attendance_id>/', delete_work_attendance, name='delete_work_attendance'),
    path('confirm-staff/', csrf_exempt(confirm_staff_status), name="confirm_staff_status"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
