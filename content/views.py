from django.shortcuts import render
from .models import Gallery
from django.views.generic import TemplateView


class GalleryView(TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Fetch the latest 4 images for the carousel
        context['latest_images'] = Gallery.objects.filter(is_active=True).order_by('-created_at')[:4]

        # Fetch all images for the grid
        context['all_images'] = Gallery.objects.filter(is_active=True).order_by('-created_at')

        return context