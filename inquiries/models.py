from django.db import models
from core.models import healthcarePackages, Services
from uuid import uuid4


class enquryBase(models.Model):
    """
    This model is used to store the user related information for the enquiry
    """

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    country_code = models.CharField(max_length=10, default="+971", blank=True)
    phone_number = models.CharField(max_length=20)
    agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    patient_ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500)
    email_sent = models.BooleanField(default=False)

    class Meta:
        abstract = True


class generalEnquiry(enquryBase):
    """
    This model is used to store the general enquiry information
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.message)[:50] + "..."

    class Meta:
        verbose_name_plural = "General Enquiries"


class healthcareEnquiry(enquryBase):
    """
    This model is used to store the healthcare enquiry information
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    package = models.ForeignKey(
        healthcarePackages, on_delete=models.CASCADE, related_name="healthcare_package"
    )
    address = models.TextField(max_length=1000)
    conditions = models.TextField(max_length=1000, null=True, blank=True)
    pref_date = models.DateField()
    pref_time = models.TimeField()

    def __str__(self):
        return str(self.package) + " - " + str(self.pref_date)

    class Meta:
        verbose_name_plural = "Healthcare Enquiries"


class serviceEnquiry(enquryBase):
    """
    This model is used to store the service enquiry information
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    service = models.ForeignKey(
        Services, on_delete=models.CASCADE, related_name="service"
    )
    source = models.CharField(max_length=400)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.service) + " - " + str(self.message)[:50] + "..."

    class Meta:
        verbose_name_plural = "Service Enquiries"
