from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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