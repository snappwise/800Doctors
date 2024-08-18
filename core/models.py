from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch.dispatcher import receiver
from uuid import uuid4
from django.core.exceptions import ValidationError


class seoBase(models.Model):
    """
    This model is used to store the SEO related information for the website
    """

    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True


class Services(seoBase):
    """
    This model is used to store the services offered by the company
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    service_name = models.CharField(max_length=150)
    icon_link = models.ImageField(upload_to="icons/")
    service_card_description = models.TextField(max_length=300)
    service_photo = models.ImageField(upload_to="service_photos/")
    service_details = RichTextField()
    service_quote = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.service_name)

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "Services"


@receiver(pre_delete, sender=Services)
def mymodel_delete_services(sender, instance, **kwargs):
    instance.icon_link.delete(False)
    instance.service_photo.delete(False)


@receiver(post_init, sender=Services)
def backup_image_path_services(sender, instance, **kwargs):
    instance._current_imagen_file1 = instance.icon_link
    instance._current_imagen_file2 = instance.service_photo


@receiver(post_save, sender=Services)
def delete_old_image_services(sender, instance, **kwargs):
    if hasattr(instance, "_current_imagen_file1"):
        if instance._current_imagen_file1 != instance.icon_link:
            instance._current_imagen_file1.delete(save=False)
    if hasattr(instance, "_current_imagen_file2"):
        if instance._current_imagen_file2 != instance.service_photo:
            instance._current_imagen_file2.delete(save=False)


class healthcareCategories(models.Model):
    """
    This model is used to store the healthcare categories
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category_name = models.CharField(max_length=150)
    category_description = models.TextField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.category_name)

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "Healthcare Categories"


class healthcarePackages(seoBase):
    """
    This model is used to store the healthcare packages
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(
        healthcareCategories, on_delete=models.CASCADE, related_name="category"
    )
    healthcare_card_photo = models.ImageField(upload_to="healthcare_card_photos/")
    package_name = models.CharField(max_length=150)
    package_description = models.TextField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.package_name)

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "Healthcare Packages"


@receiver(pre_delete, sender=healthcarePackages)
def mymodel_delete_healthcare(sender, instance, **kwargs):
    instance.healthcare_card_photo.delete(False)


@receiver(post_init, sender=healthcarePackages)
def backup_image_path_healthcare(sender, instance, **kwargs):
    instance._current_imagen_file = instance.healthcare_card_photo


@receiver(post_save, sender=healthcarePackages)
def delete_old_image_healthcare(sender, instance, **kwargs):
    if hasattr(instance, "_current_imagen_file"):
        if instance._current_imagen_file != instance.healthcare_card_photo:
            instance._current_imagen_file.delete(save=False)


class Faqs(seoBase):
    """
    This model is used to store the frequently asked questions
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    question = models.TextField(max_length=300)
    answer = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)
    
    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "FAQs"


class Testimonials(seoBase):
    """
    This model is used to store the testimonials
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    rating = models.FloatField()
    testimonial = models.TextField(max_length=500)
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.testimonial)[:50] + "..."

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5")

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "Testimonials"


class Journey(seoBase):
    """
    This model is used to store the journey of the company
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    journey_title = models.CharField(max_length=150)
    journey_description = models.TextField(max_length=500)
    sequence = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.journey_title)
    
    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "Journey"
