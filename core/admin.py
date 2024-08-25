from django.contrib import admin
from core.models import (
    Services,
    healthcareCategories,
    healthcarePackages,
    Testimonials,
    Faqs,
    Journey,
)
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars


class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "service_name",
        "icon_link_tag",
        "service_card_description",
        "service_photo_tag",
        "created_at",
        "is_active",
        "Action",
    )
    search_fields = ("service_name", "service_card_description")
    list_filter = ("is_active",)
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def service_photo_tag(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" />'.format(obj.service_photo.url)
        )

    service_photo_tag.short_description = "Service Image"

    def icon_link_tag(self, obj):
        return format_html(
            """<script src="https://cdn.lordicon.com/lordicon.js"></script>
            <lord-icon
                src="{}"
                trigger="hover"
                delay="2000"
                style="width:100px;height:100px">
            </lord-icon>""".format(
                obj.icon_link
            )
        )

    icon_link_tag.short_description = "Icon Link"

    def service_name(self, obj):
        try:
            return truncatechars(obj.service_name, 50)
        except Exception:
            return obj.service_name

    def service_card_description(self, obj):
        try:
            return truncatechars(obj.service_card_description, 50)
        except Exception:
            return obj.service_card_description

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/core/services/{obj.id}/change/" class="default">edit</a>'
        )

    def soft_delete(self, request, queryset):
        """
        Mark selected records as inactive (soft delete).
        """
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} records were successfully marked as inactive."
        )

    soft_delete.short_description = "Mark selected records as inactive"

    def restore(self, request, queryset):
        """
        Restore selected records.
        """
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} records were successfully restored."
        )

    restore.short_description = "Restore selected records"


class healthcareCategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category_name",
        "category_description",
        "created_at",
        "is_active",
        "Action",
        "know_more",
    )
    search_fields = ("category_name", "category_description")
    list_filter = ("is_active",)
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def category_name(self, obj):
        try:
            return truncatechars(obj.category_name, 50)
        except Exception:
            return obj.category_name

    def category_description(self, obj):
        try:
            return truncatechars(obj.category_description, 50)
        except Exception:
            return obj.category_description

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/core/healthcarecategories/{obj.id}/change/" class="default">edit</a>'
        )

    def soft_delete(self, request, queryset):
        """
        Mark selected records as inactive (soft delete).
        """
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} records were successfully marked as inactive."
        )

    soft_delete.short_description = "Mark selected records as inactive"

    def know_more(self, obj):
        try:
            return truncatechars(obj.know_more, 50)
        except Exception:
            return obj.know_more

    def restore(self, request, queryset):
        """
        Restore selected records.
        """
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} records were successfully restored."
        )

    restore.short_description = "Restore selected records"


class healthcarePackagesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "category",
        "package_name",
        "healthcare_card_photo_tag",
        "package_description",
        "created_at",
        "is_active",
        "Action",
    )
    search_fields = ("package_name", "package_description")
    list_filter = ("is_active", "category")
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def package_name(self, obj):
        try:
            return truncatechars(obj.package_name, 50)
        except Exception:
            return obj.package_name

    def package_description(self, obj):
        try:
            return truncatechars(obj.package_description, 50)
        except Exception:
            return obj.package_description

    def healthcare_card_photo_tag(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" />'.format(
                obj.healthcare_card_photo.url
            )
        )

    healthcare_card_photo_tag.short_description = "Healthcare Card Photo"

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/core/healthcarepackages/{obj.id}/change/" class="default">edit</a>'
        )

    def soft_delete(self, request, queryset):
        """
        Mark selected records as inactive (soft delete).
        """
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} records were successfully marked as inactive."
        )

    soft_delete.short_description = "Mark selected records as inactive"

    def restore(self, request, queryset):
        """
        Restore selected records.
        """
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} records were successfully restored."
        )

    restore.short_description = "Restore selected records"


class TestimonialsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "rating",
        "testimonial",
        "created_at",
        "is_active",
        "Action",
    )
    search_fields = ("author", "testimonial")
    list_filter = ("is_active",)
    ordering = ("-created_at", "rating")
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def author(self, obj):
        try:
            return truncatechars(obj.author, 50)
        except Exception:
            return obj.author

    def testimonial(self, obj):
        try:
            return truncatechars(obj.testimonial, 50)
        except Exception:
            return obj.testimonial

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/core/testimonials/{obj.id}/change/" class="default">edit</a>'
        )

    def soft_delete(self, request, queryset):
        """
        Mark selected records as inactive (soft delete).
        """
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} records were successfully marked as inactive."
        )

    soft_delete.short_description = "Mark selected records as inactive"

    def restore(self, request, queryset):
        """
        Restore selected records.
        """
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} records were successfully restored."
        )

    restore.short_description = "Restore selected records"


class faqsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "question",
        "answer",
        "created_at",
        "is_active",
        "Action",
    )
    search_fields = ("question", "answer")
    list_filter = ("is_active",)
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def question(self, obj):
        try:
            return truncatechars(obj.question, 50)
        except Exception:
            return obj.question

    def answer(self, obj):
        try:
            return truncatechars(obj.answer, 50)
        except Exception:
            return obj.answer

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/core/faqs/{obj.id}/change/" class="default">edit</a>'
        )

    def soft_delete(self, request, queryset):
        """
        Mark selected records as inactive (soft delete).
        """
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} records were successfully marked as inactive."
        )

    soft_delete.short_description = "Mark selected records as inactive"

    def restore(self, request, queryset):
        """
        Restore selected records.
        """
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} records were successfully restored."
        )

    restore.short_description = "Restore selected records"


class journeyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "journey_title",
        "journey_description",
        "sequence",
        "created_at",
        "is_active",
        "Action",
    )
    search_fields = ("journey_title", "journey_description")
    list_filter = ("is_active",)
    ordering = ("-created_at", "sequence")
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def journey_title(self, obj):
        try:
            return truncatechars(obj.journey_title, 50)
        except Exception:
            return obj.journey_title

    def journey_description(self, obj):
        try:
            return truncatechars(obj.journey_description, 50)
        except Exception:
            return obj.journey_description

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/core/journey/{obj.id}/change/" class="default">edit</a>'
        )

    def soft_delete(self, request, queryset):
        """
        Mark selected records as inactive (soft delete).
        """
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, f"{updated_count} records were successfully marked as inactive."
        )

    soft_delete.short_description = "Mark selected records as inactive"

    def restore(self, request, queryset):
        """
        Restore selected records.
        """
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, f"{updated_count} records were successfully restored."
        )

    restore.short_description = "Restore selected records"


admin.site.register(Services, ServicesAdmin)
admin.site.register(healthcareCategories, healthcareCategoriesAdmin)
admin.site.register(healthcarePackages, healthcarePackagesAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(Faqs, faqsAdmin)
admin.site.register(Journey, journeyAdmin)
