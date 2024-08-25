from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import requests

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

        # Verify reCAPTCHA
        recaptcha_response = request.data.get("g-recaptcha-response")
        recaptcha_secret_key = settings.RECAPTCHA_SECRET_KEY
        recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

        recaptcha_data = {
            "secret": recaptcha_secret_key,
            "response": recaptcha_response,
        }

        recaptcha_response = requests.post(recaptcha_url, data=recaptcha_data)
        recaptcha_result = recaptcha_response.json()

        if not recaptcha_result.get("success"):
            return Response(
                {
                    "status": "error",
                    "message": "reCAPTCHA verification failed.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        else:
            print("Validation Errors:", serializer.errors)  # Log validation errors
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
        recaptcha_response = data.get("recaptcha")

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

        # Proceed with your existing form handling
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

        print("Validation Errors:", serializer.errors)
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
        data['agreement'] = data['terms']

        print("Data:", data)

        # Verify reCAPTCHA
        recaptcha_response = request.data.get("g-recaptcha-response")
        recaptcha_secret_key = settings.RECAPTCHA_SECRET_KEY
        recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"

        recaptcha_data = {
            "secret": recaptcha_secret_key,
            "response": recaptcha_response,
        }

        recaptcha_response = requests.post(recaptcha_url, data=recaptcha_data)
        recaptcha_result = recaptcha_response.json()

        if not recaptcha_result.get("success"):
            return Response(
                {
                    "status": "error",
                    "message": "reCAPTCHA verification failed.",
                    "errors": recaptcha_result,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        print("Validation Errors:", serializer.errors)
        return Response(
            {
                "status": "error",
                "message": "Failed to submit enquiry.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
