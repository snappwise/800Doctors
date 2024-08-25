from uuid import uuid4
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

dynamic_type_choices = (
    ("Landing Page", "Landing Page"),
    ("Core", "Core"),
    ("Inquiries", "Inquiries"),
    ("Content", "Content"),
)


class DynamicLinking(models.Model):
    """
    This model is used to store the dynamic URLs for the website
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    type = models.CharField(
        max_length=200, choices=dynamic_type_choices, default="Landing Page"
    )
    name = models.CharField(max_length=255, unique=True)
    path = models.SlugField(max_length=500, unique=True)
    view_name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.path or self.path == slugify(self.name):
            self.path = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        if not self.path == slugify(self.path):
            raise ValidationError(
                "Path must be SEO-friendly (lowercase, hyphens only)."
            )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Dynamic Linking"
