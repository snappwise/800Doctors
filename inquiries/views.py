from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import requests

from inquiries.serializers import (
    generalEnquirySerializer,
    healthcareEnquirySerializer,
    serviceEnquirySerializer,
)


def get_client_ip(request):
    """
    This function is used to get the client IP address from the request.
    """
    try:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    except Exception as e:
        print("Failed to get client IP:", e)
        return "Not Found"


def send_alert_email(title, data, form_name):
    """
    This function sends an email using DreamHost SMTP.
    """
    try:
        template_name = "email.html"
        context = {
            "title": title,
            "message1": f"""Hello {data['first_name'] + ' ' + data['last_name']}!""",
            "message2": f"""Thank you for reaching out to 800Doctor. We have received your <span style="text-decoration: underline;"></span>{form_name}</span> and our team is reviewing the details.""",
            "message3": """<br>One of our representatives will get back to you shortly to assist with your request.<br>
                If you need immediate assistance or have any urgent questions, please don't hesitate to contact us at +971 800 362867<br>""",
        }

        convert_to_html_content_user = render_to_string(
            template_name=template_name, context=context
        )
        plain_message = strip_tags(convert_to_html_content_user)

        message_user = EmailMultiAlternatives(
            "Your " + title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [data["user_email"]],
        )

        # Adding each key-value pair in the `data` dictionary
        message_lines = []
        for key, value in data.items():
            if (
                key not in ["terms", "recaptcha", "g-recaptcha-response", "agreement"]
                and value
            ):
                message_lines.append(f"\n{key.capitalize()}: {value}<br>")

        message_lines.append("<br>Thank You!</p>")
        context["message1"] = ""
        context[
            "message2"
        ] = f"""<p>Hello Admin,<br>
            A new {form_name} has been submitted by <span>{data['first_name']} {data['last_name']}</span>.<br><br>"""
        context["message3"] = "".join(message_lines)

        convert_to_html_content_admin = render_to_string(
            template_name=template_name, context=context
        )
        plain_message = strip_tags(convert_to_html_content_admin)

        message_admin = EmailMultiAlternatives(
            "New " + title,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
        )

        message_user.attach_alternative(convert_to_html_content_user, "text/html")
        emails_sent_user = message_user.send()

        message_admin.attach_alternative(convert_to_html_content_admin, "text/html")
        emails_sent_admin = message_admin.send()

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
            data["patient_ip"] = get_client_ip(request)
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

            recaptcha_response = requests.post(
                recaptcha_url, data=recaptcha_data, timeout=5
            )
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
            emails_sent = send_alert_email(
                "General Enquiry Form Submission", data, "General Enquiry"
            )
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
        try:
            data = request.data.copy()
            recaptcha_response = data.get("recaptcha")

            # Verify reCAPTCHA
            recaptcha_secret_key = settings.RECAPTCHA_SECRET_KEY
            recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
            recaptcha_data = {
                "secret": recaptcha_secret_key,
                "response": recaptcha_response,
            }
            recaptcha_result = requests.post(
                recaptcha_url, data=recaptcha_data, timeout=5
            ).json()

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
            data["patient_ip"] = get_client_ip(request)
            data["user_agent"] = request.META.get("HTTP_USER_AGENT", "not found")
            data["agreement"] = data["terms"]

            print("User Email:", data["user_email"])
            emails_sent = send_alert_email(
                "Healthcare Enquiry Form Submission", data, "Healthcare Enquiry"
            )
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

        except Exception as e:
            print("Failed to submit enquiry:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Something went wrong.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class serviceEnquiryView(APIView):
    """
    This view is used to store the service enquiry information
    """

    def post(self, request):
        try:
            data = request.data.copy()
            data["email_sent"] = True
            data["patient_ip"] = get_client_ip(request)
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

            recaptcha_response = requests.post(
                recaptcha_url, data=recaptcha_data, timeout=5
            )
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
            emails_sent = send_alert_email(
                "Service Enquiry Form Submission", data, "Service Enquiry"
            )
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

        except Exception as e:
            print("Failed to submit enquiry:", e)
            return Response(
                {
                    "status": "error",
                    "message": "Something went wrong.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
