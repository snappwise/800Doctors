from django.shortcuts import render
from .models import Gallery

def gallery_view(request):
    # Fetch the latest 4 images for the carousel
    latest_images = Gallery.objects.filter(is_active=True).order_by('-created_at')[:4]
    
    # Fetch all images for the grid
    all_images = Gallery.objects.filter(is_active=True).order_by('-created_at')
    
    # Pass both querysets to the template
    context = {
        'latest_images': latest_images,
        'all_images': all_images
    }
    return render(request, 'gallery.html', context)