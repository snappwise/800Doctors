from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
import requests
from django.views.generic import ListView, DetailView, TemplateView
from django.templatetags.static import static
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import logging
from inquiries.views import get_client_ip, send_alert_email

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
    This view is used to fetch the services information.
    """

    def get(self, request):
        try:
            # Fetch active services
            services = Services.objects.filter(is_active=True)
            # Serialize the service data
            serializer = ServicesSerializer(services, many=True)
            # Return a successful response with serialized data
            return Response(
                {
                    "status": "success",
                    "message": "Services fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # Log the error message (consider using logging instead of print)
            print("Error fetching services:", e)
            # Return an error response
            return Response(
                {
                    "status": "error",
                    "message": "Failed to fetch services.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


logger = logging.getLogger(__name__)


class HealthcarePackagesView(APIView):
    """
    This view is used to fetch the healthcare packages information.
    """

    def get(self, request):
        try:
            # Fetch active healthcare packages
            packages = healthcarePackages.objects.filter(is_active=True)
            # Serialize the package data
            serializer = healthcarePackagesSerializer(packages, many=True)
            # Return a successful response with serialized data
            return Response(
                {
                    "status": "success",
                    "message": "Healthcare Packages fetched successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            # Log the error message
            logger.error("Error fetching healthcare packages: %s", e)
            # Return an error response
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
            data["patient_ip"] = get_client_ip(request)
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


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve and serialize services, limiting to 7
        services = Services.objects.all()[:7]
        serializer = ServicesSerializer(services, many=True)
        serialized_services = serializer.data

        # Retrieve and serialize FAQs
        faqs = Faqs.objects.filter(is_active=True).order_by("created_at")

        # Retrieve and serialize testimonials
        testimonials = Testimonials.objects.filter(is_active=True)
        testimonial_serializer = TestimonialsSerializer(testimonials, many=True)
        serialized_testimonials = testimonial_serializer.data

        # Retrieve the reCAPTCHA site key from settings
        recaptcha_site_key = getattr(settings, "RECAPTCHA_SITE_KEY", None)
        if not recaptcha_site_key:
            raise ImproperlyConfigured("No recaptcha site key found.")

        # Update context with the data
        context.update(
            {
                "faqs": faqs,
                "services": serialized_services,
                "testimonials": serialized_testimonials,
                "recaptcha_site_key": recaptcha_site_key,
                "noindex" : True
            }
        )

        return context


class ServicesPageView(ListView):
    model = Services  # Use the correct model name
    template_name = "services.html"
    context_object_name = "services"

    def get_queryset(self):
        # Return only active services
        return Services.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Retrieve active testimonials
            context["testimonials"] = Testimonials.objects.filter(is_active=True)

            # Retrieve the reCAPTCHA site key from settings
            recaptcha_site_key = getattr(settings, "RECAPTCHA_SITE_KEY", None)
            if not recaptcha_site_key:
                raise ImproperlyConfigured("No recaptcha site key found.")
            context["recaptcha_site_key"] = recaptcha_site_key

        except Testimonials.DoesNotExist:
            context["testimonials"] = []

        return context


class ServiceDetailView(DetailView):
    model = Services  # Use the correct model name
    template_name = "service.html"
    context_object_name = "service"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the reCAPTCHA site key from settings and add it to the context
        recaptcha_site_key = getattr(settings, "RECAPTCHA_SITE_KEY", None)
        if not recaptcha_site_key:
            raise ImproperlyConfigured("No recaptcha site key found.")
        context["recaptcha_site_key"] = recaptcha_site_key

        return context


class HealthcarePackagesListView(TemplateView):
    template_name = "package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve all active packages
        try:
            all_packages = healthcarePackages.objects.filter(
                is_active=True
            ).select_related("category")

            # Categorize packages
            categorized_packages = {}
            for package in all_packages:
                category_name = package.category.category_name
                if category_name not in categorized_packages:
                    categorized_packages[category_name] = []
                categorized_packages[category_name].append(package)

            # Add context data
            context["categorized_packages"] = categorized_packages
            context["wellness_image_url"] = static("assets/images/wellnessDr.jpg")

        except healthcarePackages.DoesNotExist:
            context["categorized_packages"] = {}
            context["wellness_image_url"] = ""

        return context


class BookPackageView(ListView):
    model = healthcarePackages
    template_name = "package-booking.html"
    context_object_name = "packages"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the reCAPTCHA site key from settings and add it to the context
        recaptcha_site_key = getattr(settings, "RECAPTCHA_SITE_KEY", None)
        if not recaptcha_site_key:
            raise ImproperlyConfigured("No recaptcha site key found.")
        context["recaptcha_site_key"] = recaptcha_site_key

        return context


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Fetch and limit services to 7
            services = (
                Services.objects.all().order_by("-created_at")[:7].select_related()
            )
            serializer = ServicesSerializer(services, many=True)
            context["services"] = (
                serializer.data
            )  # Serialize only if needed in the template as JSON

            # Fetch active FAQs ordered by creation date
            context["faqs"] = Faqs.objects.filter(is_active=True).order_by("created_at")

            # Fetch active testimonials ordered by creation date
            context["testimonials"] = Testimonials.objects.filter(
                is_active=True
            ).order_by("-created_at")

        except Services.DoesNotExist:
            context["services"] = []
        except Faqs.DoesNotExist:
            context["faqs"] = []
        except Testimonials.DoesNotExist:
            context["testimonials"] = []

        return context


class AboutUsPageView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        try:
            # Retrieve and process journeys, ensuring order by sequence
            context["journeys"] = Journey.objects.filter(is_active=True).order_by(
                "sequence"
            )

            # Retrieve and process testimonials, ordered by creation date
            context["testimonials"] = Testimonials.objects.filter(
                is_active=True
            ).order_by("-created_at")

            # Retrieve the reCAPTCHA site key from settings and add it to the context
            recaptcha_site_key = getattr(settings, "RECAPTCHA_SITE_KEY", None)
            if not recaptcha_site_key:
                raise ImproperlyConfigured("No recaptcha site key found.")
            context["recaptcha_site_key"] = recaptcha_site_key

        except Journey.DoesNotExist:
            context["journeys"] = []
        except Testimonials.DoesNotExist:
            context["testimonials"] = []

        return context


class CareerPageView(TemplateView):
    template_name = "career.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Retrieve the reCAPTCHA site key from settings
        recaptcha_site_key = getattr(settings, "RECAPTCHA_SITE_KEY", None)
        if not recaptcha_site_key:
            raise ImproperlyConfigured("RECAPTCHA_SITE_KEY is not set in the settings.")
        context["recaptcha_site_key"] = recaptcha_site_key

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
