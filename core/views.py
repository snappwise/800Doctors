from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Services
from rest_framework.decorators import api_view
import requests
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, TemplateView
from django.templatetags.static import static
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication
from django.conf import settings

from core.models import (
    Services,
    healthcareCategories,
    healthcarePackages,
    Faqs,
    Testimonials,
    Journey,
)
from core.serializers import (
    ServicesSerializer,
    healthcareCategoriesSerializer,
    healthcarePackagesSerializer,
    FaqsSerializer,
    TestimonialsSerializer,
    JourneySerializer,
)


class ServicesView(APIView):
    """
    This view is used to store the services information
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
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


class healthcarePackagesView(APIView):
    """
    This view is used to store the healthcare packages information
    """

    def get(self, request):
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


class FaqsView(APIView):
    """
    This view is used to store the faqs information
    """

    def get(self, request):
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


class TestimonialsView(APIView):
    """
    This view is used to store the testimonials information
    """

    def get(self, request):
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


class JourneyView(APIView):
    """
    This view is used to store the journey information
    """

    def get(self, request):
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


class ServiceListView(APIView):

    def get(self, request, format=None):
        request_domain = request.get_host()
        if request_domain != settings.ALLOWED_HOSTS[0]:
            return Response(
                {"detail": "Forbidden: Invalid host"}, status=status.HTTP_403_FORBIDDEN
            )
        services = Services.objects.all()[:7]  # Limit to 7 services
        serializer = ServicesSerializer(services, many=True)
        return Response(serializer.data)


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
    model = Services
    template_name = "service.html"
    context_object_name = "service"


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
    model = healthcarePackages
    template_name = "package-booking.html"
    context_object_name = "packages"


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

        # Generate a list of star ratings for each testimonial
        for testimonial in testimonials:
            testimonial.stars = [1, 2, 3, 4, 5]  # List of star indices

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

        return context