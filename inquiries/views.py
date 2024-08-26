from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import requests

from inquiries.serializers import (
    generalEnquirySerializer,
    healthcareEnquirySerializer,
    serviceEnquirySerializer,
)

from django.core.mail import EmailMultiAlternatives


def send_alert_email(title, data, form_name):
    """
    This function sends an email using DreamHost SMTP.
    """
    try:
        template_name = "email-template.html"
        context = {
            "title": title,
            "message": f"""

            <h1>Hello {data['first_name'] + " " + data['last_name']},</h1>
            <h3>Thank you for filling out {form_name} form</h3>""",
        }

        convert_to_html_content_user = render_to_string(
            template_name=template_name,
            # context=context
        )
        plain_message = strip_tags(convert_to_html_content_user)

        message_user = EmailMultiAlternatives(
            title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [data["user_email"]],
        )

        message_lines = [
            "<p>Hello Admin,<br>",
            f"A new enquiry has been submitted by <span>{data['first_name']} {data['last_name']}</span>.<br><br>",
        ]

        # Adding each key-value pair in the `data` dictionary
        for key, value in data.items():
            if key not in ["terms", "recaptcha", "g-recaptcha-response"] and value:
                message_lines.append(f"\n{key.capitalize()}: {value}<br>")

        message_lines.append("<br>Thank You!</p>")
        context["message"] = "".join(message_lines)

        convert_to_html_content_admin = render_to_string(
            template_name=template_name,
            # context=context
        )
        plain_message = strip_tags(convert_to_html_content_admin)

        message_admin = EmailMultiAlternatives(
            title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [data["user_email"]],
        )

        message_user.attach_alternative(convert_to_html_content_admin, "text/html")
        emails_sent_admin = message_user.send()

        message_admin.attach_alternative(convert_to_html_content_user, "text/html")
        emails_sent_user = message_admin.send()

        print("Emails sent to admin:", emails_sent_admin)
        print("Emails sent to user:", emails_sent_user)
    except Exception as e:
        print("Failed to send email:", e)
        emails_sent_admin = 0

    return emails_sent_admin


class generalEnquiryView(APIView):
    """
    This view is used to store the general enquiry information
    """

    def post(self, request):
        try:
            data = request.data.copy()
            data["patient_ip"] = request.META.get("REMOTE_ADDR")
            data["user_agent"] = request.META.get("HTTP_USER_AGENT", "not found")
            data["agreement"] = data["terms"]

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
                print("here!")
                return Response(
                    {
                        "status": "error",
                        "message": "reCAPTCHA verification failed.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            print("User Email:", data["user_email"])
            emails_sent = send_alert_email("New General Enquiry", data, "Contact US")
            data["email_sent"] = False
            if emails_sent == 1:
                data["email_sent"] = True
                print("Email sent successfully")

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

        except Exception as e:
            print("Failed to submit enquiry:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Something went wrong.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        data["agreement"] = data["terms"]

        print("User Email:", data["user_email"])
        emails_sent = send_alert_email("New General Enquiry", data, "Contact US")
        data["email_sent"] = False
        if emails_sent == 1:
            data["email_sent"] = True
            print("Email sent successfully")
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
        data["agreement"] = data["terms"]

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
        print("User Email:", data["user_email"])
        emails_sent = send_alert_email("New General Enquiry", data, "Contact US")
        data["email_sent"] = False
        if emails_sent == 1:
            data["email_sent"] = True
            print("Email sent successfully")
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
