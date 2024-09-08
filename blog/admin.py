from typing import Any
from django.contrib import admin
from blog.models import blogCategories, Blog
from django.utils.html import format_html
from django.template.defaultfilters import truncatechars


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "category_name",
        "category_remark",
        "is_active",
        "created_at",
        "Action",
    )
    list_filter = ("category_name", "is_active")
    search_fields = ("category_name", "category_remark")
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/blog/blog/{obj.id}/change/" class="default">edit</a>'
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


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "blog_card_title",
        "category",
        "blogger",
        "blog_card_image_tag",
        "blog_card_description",
        "blog_data_formatted",
        "blog_seo_title",
        "is_active",
        "created_at",
        "Action",
    )
    list_filter = ("category", "blogger", "is_active")
    search_fields = (
        "blog_card_title",
        "blog_card_description",
        "blog_data",
        "blog_seo_title",
    )
    ordering = ("-created_at",)
    actions = ["soft_delete", "restore"]
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        obj.blogger = request.user
        super().save_model(request, obj, form, change)

    def blog_card_image_tag(self, obj):
        return format_html(
            '<a href="{}" target="_blank"><img src="{}" width="100" height="100" /></a>',
            obj.blog_card_image.url,
            obj.blog_card_image.url,
        )
    
    def blog_card_description(self, obj):
        return truncatechars(obj.blog_card_description, 50)

    def blog_data_formatted(self, obj):
        return truncatechars(format_html(obj.blog_data), 50)

    def Action(self, obj):
        return format_html(
            f'<a href = "/admin/blog/blog/{obj.id}/change/" class="default">edit</a>'
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


admin.site.register(blogCategories, BlogCategoryAdmin)
admin.site.register(Blog, BlogAdmin)
