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
from dynamic_linking.models import DynamicLinking


def dynamic_urlpatterns():
    """
    This function generates the dynamic URL patterns for the website
    """
    patterns = []
    for url in DynamicLinking.objects.all():
        # view = getattr(core_views, url.view_name, None)

        patterns.append(path(url.path, IndexPageView.as_view(), name=url.name))
    return patterns


urlpatterns = [
    # API services
    path("api/six-services/", ServiceListView.as_view(), name="service-list"),
    # HTML pages
    path("services/", ServicesPageView.as_view(), name="services"),
    path("services/<uuid:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path(
        "healthcare-packages/",
        HealthcarePackagesListView.as_view(),
        name="healthcare_packages",
    ),
    path("healthcare-package-booking/", BookPackageView.as_view(), name="book_packages"),
    path("about-us/", AboutUsPageView.as_view(), name="about-us"),
    path("", HomeView.as_view(), name="home"),
    *dynamic_urlpatterns(),
]
