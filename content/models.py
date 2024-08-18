from django.db import models
from django.db.models.signals import pre_delete, post_init, post_save
from django.dispatch.dispatcher import receiver
from uuid import uuid4


class seoBase(models.Model):
    """
    This model is used to store the SEO related information for the website
    """

    meta_title = models.CharField(max_length=100, blank=True, null=True)
    meta_description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        abstract = True


class Gallery(seoBase):
    """
    This model is used to store the services offered by the company
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image_name = models.CharField(max_length=200)
    gallery_image = models.ImageField(upload_to="gallery/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image_name)

    def soft_delete(self):
        self.is_active = False
        self.save()

    class Meta:
        verbose_name_plural = "Gallery"


@receiver(pre_delete, sender=Gallery)
def mymodel_delete_gallery(sender, instance, **kwargs):
    instance.gallery_image.delete(False)


@receiver(post_init, sender=Gallery)
def backup_image_path_gallery(sender, instance, **kwargs):
    instance._current_imagen_file1 = instance.gallery_image


@receiver(post_save, sender=Gallery)
def delete_old_image_gallery(sender, instance, **kwargs):
    if hasattr(instance, "_current_imagen_file1"):
        if instance._current_imagen_file1 != instance.gallery_image:
            instance._current_imagen_file1.delete(save=False)
