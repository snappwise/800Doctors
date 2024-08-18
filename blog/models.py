from django.db import models
from ckeditor.fields import RichTextField
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


class blogCategories(models.Model):
    """
    This model is used to store the blog categories
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category_name = models.CharField(max_length=150)
    category_remark = models.TextField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.category_name)


class Blog(seoBase):
    """
    This model is used to store the services offered by the company
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    category = models.ForeignKey(
        blogCategories, on_delete=models.CASCADE, related_name="blog_category"
    )
    blog_card_image = models.ImageField(upload_to="blog_card_photos/")
    blog_card_title = models.CharField(max_length=250)
    blog_card_description = models.TextField(max_length=500)
    blog_data = RichTextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.blog_card_title)[:50] + "..."


@receiver(pre_delete, sender=Blog)
def mymodel_delete_blog(sender, instance, **kwargs):
    instance.blog_card_image.delete(False)


@receiver(post_init, sender=Blog)
def backup_image_path_blog(sender, instance, **kwargs):
    instance._current_imagen_file1 = instance.blog_card_image


@receiver(post_save, sender=Blog)
def delete_old_image_blog(sender, instance, **kwargs):
    if hasattr(instance, "_current_imagen_file1"):
        if instance._current_imagen_file1 != instance.blog_card_image:
            instance._current_imagen_file1.delete(save=False)
