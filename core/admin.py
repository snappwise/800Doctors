from django.contrib import admin
from core.models import (
    Services,
    healthcareCategories,
    healthcarePackages,
    Testimonials,
    Faqs,
    # Journey,
    NewsletterSubscription,
    CareerPage,
    CareerOpenings,
    AdditionalDocument,
)
from django.utils.html import format_html
from django.forms import BaseInlineFormSet
from django import forms
import boto3
from botocore.exceptions import NoCredentialsError
from django.forms import ModelForm
from django.template.defaultfilters import truncatechars
from django.conf import settings


def generate_signed_url(file_object):
    """
    Generate a signed URL for downloading files from S3
    Args:
        file_object: Django FieldFile object (e.g., instance.resume)
    """
    if not file_object or not file_object.name:
        return None

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        # Get the complete file path including any prefix/folder structure
        file_path = str(file_object.name).strip()
        if not file_path:
            return None

        # Ensure the file path starts with the media location if needed
        if hasattr(file_object.storage, "location"):
            location = file_object.storage.location.strip("/")
            if location and not file_path.startswith(location):
                file_path = f"{location}/{file_path}"

        print(f"Generating signed URL for key: {file_path}")  # Debug print

        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": file_path},
            ExpiresIn=3600,
        )
        return url
    except Exception as e:
        print(f"Error generating signed URL: {e}")
        return None


class ServicesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "service_name",
        "icon_link_tag",
        "service_card_description",
        "service_photo_tag",
        "service_seo_title",
        "created_at",
        "is_active",
        "Action",
    )
    search_fields = ("service_name", "service_card_description", "service_seo_title")
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


# class journeyAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "journey_title",
#         "journey_description",
#         "sequence",
#         "created_at",
#         "is_active",
#         "Action",
#     )
#     search_fields = ("journey_title", "journey_description")
#     list_filter = ("is_active",)
#     ordering = ("-created_at", "sequence")
#     actions = ["soft_delete", "restore"]
#     list_per_page = 10

#     def journey_title(self, obj):
#         try:
#             return truncatechars(obj.journey_title, 50)
#         except Exception:
#             return obj.journey_title

#     def journey_description(self, obj):
#         try:
#             return truncatechars(obj.journey_description, 50)
#         except Exception:
#             return obj.journey_description

#     def Action(self, obj):
#         return format_html(
#             f'<a href = "/admin/core/journey/{obj.id}/change/" class="default">edit</a>'
#         )

#     def soft_delete(self, request, queryset):
#         """
#         Mark selected records as inactive (soft delete).
#         """
#         updated_count = queryset.update(is_active=False)
#         self.message_user(
#             request, f"{updated_count} records were successfully marked as inactive."
#         )

#     soft_delete.short_description = "Mark selected records as inactive"

#     def restore(self, request, queryset):
#         """
#         Restore selected records.
#         """
#         updated_count = queryset.update(is_active=True)
#         self.message_user(
#             request, f"{updated_count} records were successfully restored."
#         )

#     restore.short_description = "Restore selected records"


class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "created_at")
    search_fields = ("email",)
    ordering = ("-created_at",)
    list_per_page = 10


class AdditionalDocumentAdmin(admin.ModelAdmin):
    list_display = ("career_page", "document_tag", "uploaded_at")
    search_fields = ("career_page__full_name", "career_page__user_email")
    list_filter = ("uploaded_at",)
    ordering = ("-uploaded_at",)
    list_per_page = 10

    def document_tag(self, obj):
        if not obj.file:
            return "No document available"

        try:
            # Debug prints
            print(f"document name: {obj.file.name}")
            print(f"document url: {obj.file.url}")
            print(f"document storage: {obj.file.storage}")

            url = generate_signed_url(obj.file)
            if url:
                return format_html(
                    '<a href="{}" target="_blank">Download Document</a>', url
                )
            return "URL generation failed"
        except Exception as e:
            print(f"Error in document_url: {e}")
            return f"Error: {str(e)}"

    document_tag.short_description = "Document"


class AdditionalDocumentForm(ModelForm):
    class Meta:
        model = AdditionalDocument
        fields = ["file"]


class AdditionalDocumentFormSet(BaseInlineFormSet):
    def clean(self):
        """Handle multiple file uploads during cleaning."""
        super().clean()

        # Get the first form with files
        forms_with_files = [f for f in self.forms if f.files]
        if not forms_with_files:
            return

        form = forms_with_files[0]
        files = form.files.getlist("file")

        # If we have multiple files
        if len(files) > 1:
            # First file stays with the original form
            form.cleaned_data = {"file": files[0], "career_page": self.instance}

            # Create additional forms for remaining files
            for file in files[1:]:
                # Create a new form instance
                new_form = self.form(
                    {},
                    {"file": file},
                    prefix=f"{self.prefix}-{self.total_form_count()}",
                    instance=self.model(),
                )
                # Set the cleaned data
                new_form.is_valid()
                new_form.cleaned_data = {"file": file, "career_page": self.instance}
                self.forms.append(new_form)
                # Update total forms count
                self.total_form_count = lambda c=self.total_form_count() + 1: c

    def save_new(self, form, commit=True):
        """Save new instances."""
        if not form.cleaned_data:
            return None

        instance = self.model(
            career_page=self.instance, file=form.cleaned_data.get("file")
        )
        if commit:
            instance.save()
        return instance


class AdditionalDocumentInline(admin.TabularInline):
    model = AdditionalDocument
    formset = AdditionalDocumentFormSet
    form = AdditionalDocumentForm
    extra = 1
    fields = ("file", "uploaded_at")
    readonly_fields = ("uploaded_at",)

    class Media:
        js = ("scripts/multiple_file_upload.js",)


# class AdditionalDocumentForm(ModelForm):
#     class Meta:
#         model = AdditionalDocument
#         fields = ["file"]


# class AdditionalDocumentFormSet(BaseInlineFormSet):
#     def clean(self):
#         """Handle multiple file uploads during cleaning"""
#         super().clean()

#         # Get the first form with files
#         forms_with_files = [f for f in self.forms if f.files]
#         if not forms_with_files:
#             return

#         form = forms_with_files[0]
#         files = form.files.getlist("file")

#         # If we have multiple files
#         if len(files) > 1:
#             # First file stays with the original form
#             form.cleaned_data = {"file": files[0], "career_page": self.instance}

#             # Create additional forms for remaining files
#             for file in files[1:]:
#                 # Create a new form instance
#                 new_form = self.form(
#                     {},
#                     {"file": file},
#                     prefix=f"{self.prefix}-{self.total_form_count()}",
#                     instance=self.model(),
#                 )
#                 # Set the cleaned data
#                 new_form.is_valid()
#                 new_form.cleaned_data = {"file": file, "career_page": self.instance}
#                 self.forms.append(new_form)
#                 # Update total forms count
#                 self.total_form_count = lambda c=self.total_form_count() + 1: c

#     def save_new(self, form, commit=True):
#         """Save new instances"""
#         if not form.cleaned_data:
#             return None

#         instance = self.model(
#             career_page=self.instance, file=form.cleaned_data.get("file")
#         )
#         if commit:
#             instance.save()
#         return instance


# class AdditionalDocumentInline(admin.TabularInline):
#     model = AdditionalDocument
#     formset = AdditionalDocumentFormSet
#     form = AdditionalDocumentForm
#     extra = 1
#     fields = ("file", "uploaded_at")
#     readonly_fields = ("uploaded_at",)

#     class Media:
#         js = ("scripts/multiple_file_upload.js",)


class CareerPageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "user_email",
        "phone_number",
        # "resume_tag",
        "resume_url",
        "message_excerpt",
        "created_at",
        "additional_documents_list",
    )
    search_fields = ("full_name", "user_email", "phone_number")
    list_filter = ("created_at", "email_sent")
    ordering = ("-created_at",)
    list_per_page = 10
    inlines = [AdditionalDocumentInline]

    def resume_url(self, obj):
        if not obj.resume:
            return "No resume available"

        try:
            # Debug prints
            print(f"Resume name: {obj.resume.name}")
            print(f"Resume url: {obj.resume.url}")
            print(f"Resume storage: {obj.resume.storage}")

            url = generate_signed_url(obj.resume)
            if url:
                return format_html(
                    '<a href="{}" target="_blank">Download Resume</a>', url
                )
            return "URL generation failed"
        except Exception as e:
            print(f"Error in resume_url: {e}")
            return f"Error: {str(e)}"

    resume_url.short_description = "Resume Link"

    def resume_tag(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" target="_blank">View Resume</a>', obj.resume.url
            )
        return "No Resume Uploaded"

    def message_excerpt(self, obj):
        return truncatechars(obj.cover_letter, 50)

    def additional_documents_list(self, obj):
        docs = obj.additional_documents.all()
        print("\n number of additional documents: ", docs)
        if docs:
            return format_html(
                "<br>".join(
                    [
                        f'<a href="{doc.file.url}" target="_blank">Document {index + 1}</a>'
                        for index, doc in enumerate(docs)
                    ]
                )
            )
        return "No Additional Documents"


class CareerOpeningsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        "position_name",
        "category",
        "available_pos",
        "status",
        "created_at",
        "image_preview",
    )

    # Add filters to the admin sidebar
    list_filter = ("status", "category")

    # Add search functionality
    search_fields = ("position_name", "category")

    # Fields to be editable directly in the list view
    list_editable = ("status", "available_pos")

    # Fields to display in the detail view
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "position_name",
                    "position_desc",
                    "category",
                    "available_pos",
                    "status",
                    "position_image",
                    "image_preview",
                )
            },
        ),
        (
            "Content",
            {
                "fields": ("position_page_info",),
                "classes": ("wide",),
            },
        ),
        (
            "Dates",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    # Mark fields as read-only
    readonly_fields = (
        "created_at",
        "image_preview",
    )

    # Controls the ordering of the list view
    ordering = ("-created_at",)

    # Add image preview for the position image
    def image_preview(self, obj):
        if obj.position_image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" alt="{}">',
                obj.position_image.url,
                obj.position_name,
            )
        return "No image uploaded"

    image_preview.short_description = "Image Preview"


# Register the CareerOpenings model with the custom admin interface
admin.site.register(CareerOpenings, CareerOpeningsAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(healthcareCategories, healthcareCategoriesAdmin)
admin.site.register(healthcarePackages, healthcarePackagesAdmin)
admin.site.register(Testimonials, TestimonialsAdmin)
admin.site.register(Faqs, faqsAdmin)
# admin.site.register(Journey, journeyAdmin)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
admin.site.register(CareerPage, CareerPageAdmin)
admin.site.register(AdditionalDocument, AdditionalDocumentAdmin)
