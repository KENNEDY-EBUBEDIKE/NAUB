from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import check_course,\
    exam_profile, exam_attendance_sheet,\
    delete_attendance, request_exam,\
    approve_exam,\
    decline_exam_request, delete_exam_request, examination_malpractice, invigilators_attendance_sheet,\
    scan_to_invigilate, exam_profile_view

urlpatterns = [
    path('check-course/', check_course),
    path('exam-profile-view/', exam_profile_view),
    path('exam-profile/', exam_profile, name='exam_profile'),
    path('delete-attendance/<int:attendance_id>/', delete_attendance, name='delete_attendance'),
    path('attendance/', exam_attendance_sheet, name='exam_attendance_sheet'),
    path('request-exam/', request_exam, name='request_exam'),
    path('approve-exam/', approve_exam, name='approve_exam'),
    path('exam-malpractice/', examination_malpractice, name='examination_malpractice'),
    path('decline-request/<int:exam_request_id>/', decline_exam_request, name='decline_exam_request'),
    path('delete-request/<int:exam_request_id>/', delete_exam_request, name='delete_exam_request'),
    path('invigilator-attendance/', invigilators_attendance_sheet, name='invigilators_attendance_sheet'),
    path('invigilation-scan/', scan_to_invigilate, name='scan_to_invigilate'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
