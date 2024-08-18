from django.contrib import admin
from inquiries.models import generalEnquiry, healthcareEnquiry, serviceEnquiry
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars


class generalEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "user_email",
        "email_sent",
        "message",
        "created_at",
        "Action",
    )
    search_fields = ("first_name", "last_name", "phone_number", "user_email")
    list_filter = ("email_sent",)
    ordering = ("-created_at",)
    list_per_page = 10

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/inquiries/generalenquiry/{obj.id}/change/" class="default">edit</a>'
        )

    def message(self, obj):
        try:
            return truncatechars(obj.message, 50)
        except Exception:
            return obj.message


class healthcareEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "user_email",
        "email_sent",
        "package",
        "address",
        "conditions",
        "pref_date",
        "pref_time",
        "created_at",
        "Action",
    )
    search_fields = ("first_name", "last_name", "phone_number", "user_email")
    list_filter = ("email_sent",)
    date_hierarchy = "pref_date"
    ordering = ("-created_at",)
    list_per_page = 10

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/inquiries/healthcareenquiry/{obj.id}/change/" class="default">edit</a>'
        )

    def address(self, obj):
        try:
            return truncatechars(obj.address, 50)
        except Exception:
            return obj.address

    def conditions(self, obj):
        try:
            return truncatechars(obj.conditions, 50)
        except Exception:
            return obj.conditions


class serviceEnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone_number",
        "user_email",
        "service",
        "source",
        "message",
        "email_sent",
        "service",
        "created_at",
        "Action",
    )
    search_fields = ("first_name", "last_name", "phone_number", "user_email")
    list_filter = ("email_sent",)
    ordering = ("-created_at",)
    list_per_page = 10

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/inquiries/serviceenquiry/{obj.id}/change/" class="default">edit</a>'
        )

    def message(self, obj):
        try:
            return truncatechars(obj.message, 50)
        except Exception:
            return obj.message


admin.site.register(generalEnquiry, generalEnquiryAdmin)
admin.site.register(healthcareEnquiry, healthcareEnquiryAdmin)
admin.site.register(serviceEnquiry, serviceEnquiryAdmin)
