from django.urls import path
from dynamic_linking.models import DynamicLinking
from .views import (
    # ServiceListView,
    IndexPageView,
    ServicesPageView,
    ServiceDetailView,
    HealthcarePackagesListView,
    BookPackageView,
    HomeView,
    AboutUsPageView,
    CareerPageView,
    CareerPageEnquiryView,
    TermsAndConditionsView,
    PrivacyPolicyView,
    RightsView,
    DisclaimerView,
    thank_you_view,
)


def dynamic_urlpatterns():
    """
    This function generates the dynamic URL patterns for the website
    """
    patterns = []
    try:
        for url in DynamicLinking.objects.all():
            # view = getattr(core_views, url.view_name, None)

            patterns.append(path(url.path, IndexPageView.as_view(), name=url.name))
    except Exception as e:
        print(e)
    return patterns


dynamic_pattern = dynamic_urlpatterns()
if len(dynamic_pattern) == 0:
    dynamic_pattern = [
        path("doctor-on-call", IndexPageView.as_view(), name="dynamic-link")
    ]

urlpatterns = [
    # API services
    path("api/career-enquiry/", CareerPageEnquiryView.as_view(), name="career-enquiry"),
    # HTML pages
    path("services/", ServicesPageView.as_view(), name="services"),
    path("services/<uuid:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path(
        "healthcare-packages/",
        HealthcarePackagesListView.as_view(),
        name="healthcare_packages",
    ),
    path(
        "healthcare-package-booking/", BookPackageView.as_view(), name="book_packages"
    ),
    path("about-us/", AboutUsPageView.as_view(), name="about-us"),
    path("", HomeView.as_view(), name="home"),
    *dynamic_pattern,
    path("careers/", CareerPageView.as_view(), name="career-page"),
    path(
        "terms-and-conditions/",
        TermsAndConditionsView.as_view(),
        name="terms-and-conditions",
    ),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("rights/", RightsView.as_view(), name="rights"),
    path("disclaimer/", DisclaimerView.as_view(), name="disclaimer"),
    path("success/", thank_you_view, name="success"),
]
