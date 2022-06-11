from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_view
from django.views.decorators.csrf import csrf_exempt
from .views import login_view, admin_dashboard, admin_database, deactivate_admin, change_privilege, login_on_scan

urlpatterns = [
    path('', login_view, name='login_View'),
    path('login/', login_view, name='login_View'),
    path('logout/', auth_view.LogoutView.as_view(), name='LogoutView'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-database/', admin_database, name='admin_database'),
    path('change-privilege/', csrf_exempt(change_privilege), name='change_privilege'),
    path('admin-activity/<int:admin_id>/', deactivate_admin, name='deactivate_admin'),
    path('scan-login/', csrf_exempt(login_on_scan), name='login_on_scan'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
