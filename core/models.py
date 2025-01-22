from uuid import uuid4
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch.dispatcher import receiver
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.exceptions import ValidationError
from content.models import validate_image_size
from django.conf import settings
import boto3


class seoBase(models.Model):
    """
    This model is used to store the SEO related information for the website
    """

    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True


def generate_seo_title(instance):
    base_slug = slugify(instance.service_name)
    return f"{base_slug}-{str(uuid4().hex[:6])}"


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
    service_seo_title = models.SlugField(
        max_length=500,
        unique=True,
        blank=True,
        editable=True,
        # default=generate_seo_title,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.service_name)

    def save(self, *args, **kwargs):
        if not self.service_seo_title:
            base_slug = slugify(self.service_name)
            self.service_seo_title = f"{base_slug}-{str(uuid4().hex[:6])}"
        super().save(*args, **kwargs)

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
    know_more = models.TextField(max_length=400, default="")  # New field

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


job_categories = (
    ("Back Office", "Back Office"),
    ("Business Development/Marketing", "Business Development/Marketing"),
    ("Physicians (DHA, MOH)", "Physicians (DHA, MOH)"),
    (
        "Nursing (DHA RN, DHA AN, MOH RN, MOH AN)",
        "Nursing (DHA RN, DHA AN, MOH RN, MOH AN)",
    ),
    (
        "Support Staff (Driver, Housekeeping, Babysitter)",
        "Support Staff (Driver, Housekeeping, Babysitter)",
    ),
    (
        "Allied Health Professionals (Physiotherapists, Dietitians, Therapists, Health Care Assistant)",
        "Allied Health Professionals (Physiotherapists, Dietitians, Therapists, Health Care Assistant)",
    ),
)

license_choices = (
    ("DHA Eligibility", "DHA Eligibility"),
    ("MOH Evaluation", "MOH Evaluation"),
    ("License", "License"),
)
additional_job_categories = (
    ("HR", "HR"),
    ("Admin", "Admin"),
    ("Operations", "Operations"),
    ("Customer Care", "Customer Care"),
    ("Clerical", "Clerical"),
    ("Housekeeping", "Housekeeping"),
    ("Procurement", "Procurement"),
    ("Inventory", "Inventory"),
    ("Accounts", "Accounts"),
    ("Finance", "Finance"),
)


# class PrivateS3Boto3Storage(S3Boto3Storage):
#     def __init__(self, *args, **kwargs):
#         kwargs["custom_domain"] = False  # Disable public URL generation
#         kwargs["file_overwrite"] = (
#             False  # Ensure that existing files aren't overwritten without renaming
#         )
#         super().__init__(*args, **kwargs)


class PrivateS3Boto3Storage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "custom_domain": False,
                "file_overwrite": False,
                "default_acl": "private",
                "querystring_auth": True,
                "location": "media",  # Add this if you want files in a media subfolder
            }
        )
        super().__init__(*args, **kwargs)

    def url(self, name, parameters=None, expire=3600):
        """Override url method to ensure proper URL generation"""
        name = str(name).strip()
        if not name:
            return None

        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            key = self._normalize_name(name)
            print(f"Generating URL for key: {key}")  # Debug print

            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": key},
                ExpiresIn=expire,
            )
            return url
        except Exception as e:
            print(f"Error in storage url method: {e}")
            return None


class CareerPage(models.Model):
    """
    This model is used to store the career page form data.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    career_opening = models.ForeignKey(
        "CareerOpenings", on_delete=models.SET_NULL, null=True, blank=True
    )
    full_name = models.CharField(max_length=300)
    location = models.CharField(max_length=500)
    total_exp = models.CharField(max_length=250)
    user_email = models.EmailField()
    job_category = models.CharField(
        choices=job_categories + additional_job_categories, max_length=300
    )
    phone_number = models.CharField(max_length=15)
    position_apply = models.CharField(max_length=300)
    notice_period = models.CharField(max_length=300)
    license_status = models.CharField(
        null=True, blank=True, max_length=300, choices=license_choices
    )
    visa_status = models.CharField(max_length=300, blank=True, null=True)  # Optional
    languages_spoken = models.CharField(
        max_length=500, blank=True, null=True
    )  # Optional
    nationality = models.CharField(max_length=400)
    date_of_birth = models.DateField()  # Use DateField for better validation
    resume = models.FileField(
        upload_to="resumes/", storage=PrivateS3Boto3Storage()
    )  # Custom S3 storage
    cover_letter = models.TextField()
    agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} | {self.full_name}"

    def clean(self):
        # Ensure agreement is checked
        if not self.agreement:
            raise ValidationError("You must agree to the terms and conditions.")

    class Meta:
        verbose_name_plural = "Career Enquiries"
        indexes = [models.Index(fields=["created_at"])]


@receiver(pre_delete, sender=CareerPage)
def delete_resume_file(sender, instance, **kwargs):
    if instance.resume and hasattr(instance.resume, "delete"):
        # Delete the file from S3
        storage = instance.resume.storage
        storage.delete(instance.resume.name)


@receiver(post_init, sender=CareerPage)
def backup_resume_path(sender, instance, **kwargs):
    # Backup the current resume file path
    instance._current_resume_file = instance.resume


@receiver(post_save, sender=CareerPage)
def delete_old_resume(sender, instance, **kwargs):
    if hasattr(instance, "_current_resume_file"):
        # If the file has been replaced, delete the old file
        if instance._current_resume_file != instance.resume:
            # Delete the old file from S3
            storage = instance._current_resume_file.storage
            storage.delete(instance._current_resume_file.name)


class AdditionalDocument(models.Model):
    """
    Model to store additional documents for career enquiries.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    career_page = models.ForeignKey(
        CareerPage, related_name="additional_documents", on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to="additional_docs/", storage=PrivateS3Boto3Storage()
    )  # Custom S3 storage
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Document for {self.career_page.full_name} uploaded at {self.uploaded_at}"
        )


@receiver(pre_delete, sender=AdditionalDocument)
def delete_additional_document_file(sender, instance, **kwargs):
    if instance.file and hasattr(instance.file, "delete"):
        # Delete the file from S3
        storage = instance.file.storage
        storage.delete(instance.file.name)


@receiver(post_init, sender=AdditionalDocument)
def backup_additional_document_path(sender, instance, **kwargs):
    # Backup the current file path
    instance._current_additional_doc_file = instance.file


@receiver(post_save, sender=AdditionalDocument)
def delete_old_additional_document(sender, instance, **kwargs):
    if hasattr(instance, "_current_additional_doc_file"):
        # If the file has been replaced, delete the old file
        if instance._current_additional_doc_file != instance.file:
            # Delete the old file from S3
            storage = instance._current_additional_doc_file.storage
            storage.delete(instance._current_additional_doc_file.name)


career_status = (("open", "open"), ("closed", "closed"))


class CareerOpenings(models.Model):
    """
    Career to track and save career Openings/ Jobs
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    position_image = models.ImageField(upload_to="job-openings/")
    position_name = models.CharField(max_length=400)
    position_desc = models.TextField()
    position_page_info = RichTextField()
    category = models.CharField(
        max_length=300, choices=job_categories + additional_job_categories
    )
    available_pos = models.IntegerField()
    status = models.CharField(choices=career_status, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.position_name} ({self.status})"

    class Meta:
        verbose_name = "Career Opening"
        verbose_name_plural = "Career Openings"


@receiver(pre_delete, sender=CareerOpenings)
def delete_job_opening_file(sender, instance, **kwargs):
    if instance.position_image and hasattr(instance.position_image, "delete"):
        instance.position_image.delete(False)


@receiver(post_init, sender=CareerOpenings)
def backup_job_opening_path(sender, instance, **kwargs):
    # Store the current file path
    instance._current_position_image_file = instance.position_image


@receiver(post_save, sender=CareerOpenings)
def delete_old_job_opening(sender, instance, **kwargs):
    if hasattr(instance, "_current_position_image_file"):
        # If the file has been replaced, delete the old file
        if instance._current_position_image_file != instance.position_image:
            instance._current_position_image_file.delete(save=False)
