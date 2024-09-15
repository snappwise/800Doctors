from django.urls import path
from .views import BlogListView, BlogPageView, BlogDetailView

urlpatterns = [
    path("api/blogs/", BlogListView.as_view(), name="blog-list-api"),
    path("blogs/", BlogPageView.as_view(), name="blog-page"),
    path("blogs/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
]
