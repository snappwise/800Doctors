from django.contrib import admin
from content.models import Gallery
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars


class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image_name",
        "created_at",
        "is_active",
        "gallery_image_tag",
        "Action",
    )
    search_fields = ("image_name",)
    list_filter = ("is_active",)
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def gallery_image_tag(self, obj):
        return format_html(
            '<img src="{}" width="100" height="100" />'.format(obj.gallery_image.url)
        )

    gallery_image_tag.short_description = "Gallery Image"

    def image_name(self, obj):
        try:
            return truncatechars(obj.image_name, 50)
        except Exception:
            return obj.image_name

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/content/gallery/{obj.id}/change/" class="default">edit</a>'
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


admin.site.register(Gallery, GalleryAdmin)
