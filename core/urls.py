from django.urls import path
from .views import (
    ServiceListView,
    IndexPageView,
    ServicesPageView,
    ServiceDetailView,
    HealthcarePackagesListView,
    BookPackageView,
    HomeView,
    AboutUsPageView,
)

urlpatterns = [
    # API services
    path("api/six-services/", ServiceListView.as_view(), name="service-list"),
    # HTML pages
    path(
        "index_page/", IndexPageView.as_view(), name="index_page"
    ),  # HTML page to list services
    path("services_page/", ServicesPageView.as_view(), name="services"),
    path("services/<uuid:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path(
        "healthcare_page/",
        HealthcarePackagesListView.as_view(),
        name="healthcare_packages",
    ),
    path("healthcare_packagebooking/", BookPackageView.as_view(), name="book_packages"),
    path("about-us/", AboutUsPageView.as_view(), name="about-us"),
    path("", HomeView.as_view(), name="home"),
]
