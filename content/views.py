from .models import Gallery
from django.views.generic import TemplateView


class GalleryView(TemplateView):
    template_name = "gallery.html"

    def get_context_data(self, **kwargs):
        # Get the base context from the parent class
        context = super().get_context_data(**kwargs)

        # Fetch the latest 4 images for the carousel
        context['latest_images'] = Gallery.objects.filter(is_active=True).order_by('-created_at')[:6]

        # Fetch all images for the grid
        all_images = Gallery.objects.filter(is_active=True).order_by('-created_at')

        # Initialize the context with empty lists
        context['image_set1'], context['image_set2'], context['image_set3'], context['image_set4'] = [], [], [], []

        # Group images into the respective lists
        image_sets = [context['image_set1'], context['image_set2'], context['image_set3'], context['image_set4']]

        for i, image in enumerate(all_images):
            image_sets[i % 4].append(image)

        return context