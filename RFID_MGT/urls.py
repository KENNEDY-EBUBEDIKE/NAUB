"""RFID_MGT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

from .utils import scan_profile, search_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('users/', include('users.urls')),
    path('students/', include('students.urls')),
    path('staff/', include('staff.urls')),
    path('exams/', include('exams.urls')),
    path('api-auth/', include('rest_framework.urls')),

    path('scan-profile/', csrf_exempt(scan_profile), name='scan_profile'),
    path('search-profile/', csrf_exempt(search_profile), name='search_profile'),

    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    path('session_security/', include('session_security.urls')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
