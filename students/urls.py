from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import register_student,\
    student_database,\
    student_full_profile, flag_student,\
    student_profile_update,\
    error,\
    add_course, student_profile_deactivate,\
    courses_database, delete_course, update_rfid_code, students_data_upload,\
    register_course, api_test, student_lecture_attendance

urlpatterns = [
    path('student-registration/', register_student, name='register_student'),
    path('student-database/', student_database, name='student_database'),
    path('student-profile/<int:student_id>/', student_full_profile, name='student_full_profile'),
    path('student-profile-deactivate/<int:student_id>/', student_profile_deactivate, name='student_profile_deactivate'),
    path('student-profile-update/<int:student_id>/', student_profile_update, name='student_profile_update'),
    path('flag-student/<int:student_id>/', flag_student, name='flag_student'),
    path('error/', error, name='error'),
    path('add-course/', add_course),
    path('courses-database/', courses_database, name="courses_database"),
    path('delete-course/<int:course_id>/', delete_course, name='delete_course'),
    path('update-rfid-code/<int:student_id>/', csrf_exempt(update_rfid_code), name="update_rfid_code"),
    path('students-data-upload/', students_data_upload, name="students_data_upload"),
    path('register-course/<int:student_id>/', csrf_exempt(register_course), name='register_course'),
    path('lecture-attendance/', csrf_exempt(student_lecture_attendance), name='student_class_attendance'),

    # path('testing-cache/', testing_cache, name="testing_cache"),
    path('api/', api_test, name="api_test"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
