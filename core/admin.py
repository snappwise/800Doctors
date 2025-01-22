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
from django.forms import ModelForm
from django.template.defaultfilters import truncatechars


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
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">View Document</a>', obj.file.url
            )
        return "No Document Uploaded"

    document_tag.short_description = "Document"


# class CareerPageAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "full_name",
#         "user_email",
#         "phone_number",
#         "resume_tag",
#         "message_excerpt",
#         "created_at",
#     )
#     search_fields = ("full_name", "user_email", "phone_number")
#     list_filter = ("created_at", "email_sent")
#     ordering = ("-created_at",)
#     list_per_page = 10

#     def resume_tag(self, obj):
#         if obj.resume:
#             return format_html(
#                 '<a href="{}" target="_blank">View Resume</a>', obj.resume.url
#             )
#         return "No Resume Uploaded"

#     resume_tag.short_description = "Resume"

#     def message_excerpt(self, obj):
#         return truncatechars(obj.cover_letter, 50)

#     message_excerpt.short_description = "Cover Letter"


# class AdditionalDocumentFormSet(BaseInlineFormSet):
#     def save_new(self, form, commit=True):
#         # Get the files from the request
#         if form.files:
#             files = form.files.getlist("file")
#             if files:
#                 instances = []
#                 for file in files:
#                     # Create a new instance for each file
#                     instance = self.model(
#                         career_page=form.cleaned_data["career_page"], file=file
#                     )
#                     if commit:
#                         instance.save()
#                     instances.append(instance)
#                 return instances
#         return super().save_new(form, commit)


# class AdditionalDocumentInline(admin.TabularInline):
#     model = AdditionalDocument
#     formset = AdditionalDocumentFormSet
#     extra = 1
#     fields = ("file", "uploaded_at")
#     readonly_fields = ("uploaded_at",)

#     class Media:
#         js = ("scripts/multiple_file_upload.js",)  # You'll need to create this JS file


class AdditionalDocumentForm(ModelForm):
    class Meta:
        model = AdditionalDocument
        fields = ["file"]


class AdditionalDocumentFormSet(BaseInlineFormSet):
    def clean(self):
        """Handle multiple file uploads during cleaning"""
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
        """Save new instances"""
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


class CareerPageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "user_email",
        "phone_number",
        "resume_tag",
        "message_excerpt",
        "created_at",
        "additional_documents_list",
    )
    search_fields = ("full_name", "user_email", "phone_number")
    list_filter = ("created_at", "email_sent")
    ordering = ("-created_at",)
    list_per_page = 10
    inlines = [AdditionalDocumentInline]

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
