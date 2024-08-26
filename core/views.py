from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import requests
from django.views.generic import ListView, DetailView, TemplateView
from django.templatetags.static import static
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication
from django.conf import settings

from inquiries.views import send_alert_email

from core.models import (
    Services,
    healthcarePackages,
    Faqs,
    Testimonials,
    Journey,
)
from core.serializers import (
    ServicesSerializer,
    healthcarePackagesSerializer,
    FaqsSerializer,
    TestimonialsSerializer,
    JourneySerializer,
    CareerPageSerializer,
)


class ServicesView(APIView):
    """
    This view is used to store the services information
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        try:
            services = services = Services.objects.filter(is_active=True)
            serializer = ServicesSerializer(services, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Services fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Error fetching services:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch services.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class healthcarePackagesView(APIView):
    """
    This view is used to store the healthcare packages information
    """

    def get(self, request):
        try:
            packages = healthcarePackages.objects.filter(is_active=True)
            serializer = healthcarePackagesSerializer(packages, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Healthcare Packages fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Error fetching healthcare packages:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch healthcare packages.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class FaqsView(APIView):
    """
    This view is used to store the faqs information
    """

    def get(self, request):
        try:
            faqs = Faqs.objects.filter(is_active=True)
            serializer = FaqsSerializer(faqs, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Faqs fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Error fetching FAQs:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch FAQs.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class TestimonialsView(APIView):
    """
    This view is used to store the testimonials information
    """

    def get(self, request):
        try:
            testimonials = Testimonials.objects.filter(is_active=True)
            serializer = TestimonialsSerializer(testimonials, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Testimonials fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Error fetching testimonials:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch testimonials.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class JourneyView(APIView):
    """
    This view is used to store the journey information
    """

    def get(self, request):
        try:
            journey = Journey.objects.filter(is_active=True).order_by("sequence")
            serializer = JourneySerializer(journey, many=True)
            return Response(
                {
                    "status": "success",
                    "message": "Journey fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            print("Error fetching journey:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch journey.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class CareerPageEnquiryView(APIView):
    """
    This view is used to store the career page enquiry information.
    """

    def post(self, request):
        try:
            data = request.data.copy()
            recaptcha_response = data.get("g-recaptcha-response")

            # Verify reCAPTCHA
            recaptcha_secret_key = settings.RECAPTCHA_SECRET_KEY
            recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
            recaptcha_data = {
                "secret": recaptcha_secret_key,
                "response": recaptcha_response,
            }
            recaptcha_result = requests.post(recaptcha_url, data=recaptcha_data).json()

            if not recaptcha_result.get("success"):
                return Response(
                    {
                        "status": "error",
                        "message": "reCAPTCHA verification failed.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Additional data processing
            data["patient_ip"] = request.META.get("REMOTE_ADDR")
            data["user_agent"] = request.META.get("HTTP_USER_AGENT", "not found")

            emails_sent = send_alert_email(
                "Career Enquiry Form Submission", data, "Career Enquiry"
            )
            data["email_sent"] = False
            if emails_sent == 1:
                data["email_sent"] = True
                print("Email sent successfully")

            # Create or update the CareerPage entry
            serializer = CareerPageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "status": "success",
                        "message": "Career page enquiry submitted successfully.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                print("Validation Errors:", serializer.errors)
                return Response(
                    {
                        "status": "error",
                        "message": "Failed to submit enquiry.",
                        "errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            print("Error submitting career page enquiry:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Failed to submit career page enquiry.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# class ServiceListView(APIView):

#     def get(self, request, format=None):
#         requester_ip = get_client_ip(request)
#         print(f"Requester IP: {requester_ip}")
#         if requester_ip != settings.ALLOWED_HOSTS[0]:
#             return Response(
#                 {"detail": "Forbidden: Invalid host"}, status=status.HTTP_403_FORBIDDEN
#             )
#         services = Services.objects.all()[:7]  # Limit to 7 services
#         serializer = ServicesSerializer(services, many=True)
#         return Response(serializer.data)


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        request = self.request
        base_url = f"{request.scheme}://{request.get_host()}"
        api_url = f"{base_url}/api/six-services"
        try:
            response = requests.get(api_url)
            services = response.json() if response.status_code == 200 else []
        except requests.RequestException:
            services = []

        faqs = Faqs.objects.filter(is_active=True).order_by("created_at")
        testimonials = Testimonials.objects.filter(is_active=True)
        testimonials = TestimonialsSerializer(testimonials, many=True)

        # Retrieve the reCAPTCHA site key from settings
        recaptcha_site_key = settings.RECAPTCHA_SITE_KEY

        context = {
            "faqs": faqs,
            "services": services,
            "testimonials": testimonials.data,
            "recaptcha_site_key": recaptcha_site_key,  # Add the site key to context
        }
        return context


class ServicesPageView(ListView):
    model = Services
    template_name = "services.html"
    context_object_name = "services"

    def get_queryset(self):
        return Services.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["testimonials"] = Testimonials.objects.filter(is_active=True)

        # Retrieve the reCAPTCHA site key from settings
        recaptcha_site_key = settings.RECAPTCHA_SITE_KEY

        context["recaptcha_site_key"] = (
            recaptcha_site_key  # Add the site key to context
        )
        return context


class ServiceDetailView(DetailView):
    model = Services  # Make sure this is the correct model name
    template_name = "service.html"
    context_object_name = "service"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the reCAPTCHA site key from settings and add it to the context
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY

        return context


class HealthcarePackagesListView(TemplateView):
    template_name = "package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_packages = healthcarePackages.objects.filter(is_active=True)
        categorized_packages = {}

        for package in all_packages:
            category_name = package.category.category_name
            if category_name not in categorized_packages:
                categorized_packages[category_name] = []
            categorized_packages[category_name].append(package)

        context["categorized_packages"] = categorized_packages
        context["wellness_image_url"] = static("assets/images/wellnessDr.jpg")
        return context


class BookPackageView(ListView):
    model = healthcarePackages  # Make sure this is the correct model name
    template_name = "package-booking.html"
    context_object_name = "packages"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the reCAPTCHA site key from settings and add it to the context
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY

        return context


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        request = self.request

        base_url = f"{request.scheme}://{request.get_host()}"
        api_url = f"{base_url}/api/six-services"

        try:
            response = requests.get(api_url)
            services = response.json() if response.status_code == 200 else []
        except requests.RequestException:
            services = []

        faqs = Faqs.objects.filter(is_active=True).order_by("created_at")
        testimonials = Testimonials.objects.filter(is_active=True)

        context = {
            "faqs": faqs,
            "services": services,
            "testimonials": testimonials,
        }
        return context


class AboutUsPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve and process journeys
        context["journeys"] = Journey.objects.filter(is_active=True).order_by(
            "sequence"
        )

        # Retrieve and process testimonials
        testimonials = Testimonials.objects.filter(is_active=True)
        context["testimonials"] = testimonials

        # Retrieve the reCAPTCHA site key from settings and add it to the context
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY

        return context


class CareerPageView(TemplateView):
    template_name = "career.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the reCAPTCHA site key from settings and add it to the context
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY

        return context


def notfound_page(request, exception):
    """
    Custom 404 page view.
    """
    return render(request, "404.html", status=404)


class TermsAndConditionsView(TemplateView):
    """
    View for the Terms and Conditions page.
    """

    template_name = "terms-and-conditions.html"


class PrivacyPolicyView(TemplateView):
    """
    View for the Privacy Policy page.
    """

    template_name = "privacy-policy.html"


class RightsView(TemplateView):
    """
    View for the Rights and Responsibilities page.
    """

    template_name = "rights.html"


class DisclaimerView(TemplateView):
    """
    View for the Disclaimer page.
    """

    template_name = "disclaimer.html"
