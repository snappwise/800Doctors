from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from inquiries.serializers import (
    generalEnquirySerializer,
    healthcareEnquirySerializer,
    serviceEnquirySerializer,
)


class generalEnquiryView(APIView):
    """
    This view is used to store the general enquiry information
    """

    def post(self, request):
        data = request.data.copy()
        data["email_sent"] = True
        data["patient_ip"] = request.META.get("REMOTE_ADDR")
        data["user_agent"] = request.META.get("HTTP_USER_AGENT", "not found")
        serializer = generalEnquirySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Enquiry submitted successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": "error",
                "message": "Failed to submit enquiry.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class healthcareEnquiryView(APIView):
    """
    This view is used to store the healthcare enquiry information
    """

    def post(self, request):
        data = request.data.copy()
        data["email_sent"] = True
        data["patient_ip"] = request.META.get("REMOTE_ADDR")
        data["user_agent"] = request.META.get("HTTP_USER_AGENT", "not found")
        serializer = healthcareEnquirySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Enquiry submitted successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": "error",
                "message": "Failed to submit enquiry.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class serviceEnquiryView(APIView):
    """
    This view is used to store the service enquiry information
    """

    def post(self, request):
        data = request.data.copy()
        data["email_sent"] = True
        data["patient_ip"] = request.META.get("REMOTE_ADDR")
        data["user_agent"] = request.META.get("HTTP_USER_AGENT", "not found")
        serializer = serviceEnquirySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Enquiry submitted successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": "error",
                "message": "Failed to submit enquiry.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
