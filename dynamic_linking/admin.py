from django.contrib import admin
from django import forms
from django.utils.text import slugify
from dynamic_linking.models import DynamicLinking


class DynamicURLForm(forms.ModelForm):
    class Meta:
        model = DynamicLinking
        fields = "__all__"

    def clean_path(self):
        name = self.cleaned_data.get("name")
        path = self.cleaned_data.get("path")

        if not path or path == slugify(name):
            return slugify(name)
        return slugify(path)


class DynamicURLAdmin(admin.ModelAdmin):
    """
    Admin class for the DynamicURL model
    """

    form = DynamicURLForm
    list_display = ("name", "path", "view_name")
    prepopulated_fields = {"path": ("name",)}


admin.site.register(DynamicLinking, DynamicURLAdmin)
