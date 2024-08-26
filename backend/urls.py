"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve
from django.conf.urls import handler404
from inquiries.views import (
    generalEnquiryView,
    healthcareEnquiryView,
    serviceEnquiryView,
)

admin.site.site_title = "*00Doctor Admin"
admin.site.site_header = "800Doctor Admin"

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path("admin/", admin.site.urls),
    path("enquiry/general/", generalEnquiryView.as_view(), name="general-enquiry"),
    path(
        "enquiry/healthcare/",
        healthcareEnquiryView.as_view(),
        name="healthcare-enquiry",
    ),
    path("enquiry/service/", serviceEnquiryView.as_view(), name="service-enquiry"),
    path("", include("content.urls")),
    path("", include("core.urls")),
]

handler404 = "core.views.notfound_page"
