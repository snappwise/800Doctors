from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch.dispatcher import receiver
from uuid import uuid4
from django.core.exceptions import ValidationError
from content.models import validate_image_size


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
    service_name = models.CharField(max_length=200, unique=True)
    icon_link = models.URLField(max_length=200, blank=True, null=True)
    service_card_description = models.TextField(max_length=300)
    service_photo = models.ImageField(
        upload_to="service_photos/", validators=[validate_image_size]
    )
    service_details = RichTextField()
    # service_quote = models.CharField(max_length=250)
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
    if instance.service_photo and hasattr(instance.service_photo, "delete"):
        instance.service_photo.delete(False)


@receiver(post_init, sender=Services)
def backup_image_path_services(sender, instance, **kwargs):
    instance._current_imagen_file1 = instance.icon_link
    instance._current_imagen_file2 = instance.service_photo


@receiver(post_save, sender=Services)
def delete_old_image_services(sender, instance, **kwargs):
    # Check for the first image field (if it was an ImageField previously)
    if hasattr(instance, "_current_imagen_file1") and isinstance(
        instance._current_imagen_file1, models.fields.files.FieldFile
    ):
        if instance._current_imagen_file1 != instance.icon_link:
            instance._current_imagen_file1.delete(save=False)

    # Check for the second image field
    if hasattr(instance, "_current_imagen_file2") and isinstance(
        instance._current_imagen_file2, models.fields.files.FieldFile
    ):
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
    healthcare_card_photo = models.ImageField(
        upload_to="healthcare_card_photos/", validators=[validate_image_size]
    )
    package_name = models.CharField(max_length=150)
    package_description = models.TextField(max_length=300)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    know_more = models.CharField(
        max_length=400, default="Default text for know more"
    )  # New field

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
    question = models.TextField(max_length=1000)
    answer = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.question)

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "FAQs"


rating_choices = [(i / 2, i / 2) for i in range(0, 11)]


class Testimonials(seoBase):
    """
    This model is used to store the testimonials
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    rating = models.FloatField(choices=rating_choices)
    testimonial = models.TextField(max_length=500)
    author = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_rating(self):
        """Returns the integer part of the rating."""
        return int(self.rating)

    @property
    def half_rating(self):
        """Returns 1 if the rating includes .5, otherwise 0."""
        return 1 if self.rating % 1 >= 0.5 else 0

    @property
    def empty_rating(self):
        """Returns the number of empty stars (total 5 stars minus full and half ratings)."""
        return 5 - self.full_rating - self.half_rating

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


# class Journey(seoBase):
#     """
#     This model is used to store the journey of the company
#     """

#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     journey_title = models.CharField(max_length=150)
#     journey_description = models.TextField(max_length=500)
#     sequence = models.IntegerField()
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.journey_title)

#     def soft_delete(self):
#         self.is_active = False
#         self.save()

#     class Meta:
#         verbose_name_plural = "Journey"


class NewsletterSubscription(models.Model):
    """
    This model is used to store the newsletter subscription form data
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name_plural = "Newsletter Subscriptions"


class CareerPage(models.Model):
    """
    This model is used to store the career page form data
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    resume = models.FileField(upload_to="resumes/")
    message = models.TextField()
    agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        if not self.agreement:
            raise ValidationError("You must agree to the terms and conditions.")

    class Meta:
        verbose_name_plural = "Career Enquiries"


@receiver(pre_delete, sender=CareerPage)
def delete_resume_file(sender, instance, **kwargs):
    if instance.resume and hasattr(instance.resume, "delete"):
        instance.resume.delete(False)


@receiver(post_init, sender=CareerPage)
def backup_resume_path(sender, instance, **kwargs):
    instance._current_resume_file = instance.resume


@receiver(post_save, sender=CareerPage)
def delete_old_resume(sender, instance, **kwargs):
    if hasattr(instance, "_current_resume_file"):
        if instance._current_resume_file != instance.resume:
            instance._current_resume_file.delete(save=False)
