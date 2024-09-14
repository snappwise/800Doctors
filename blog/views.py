from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blog.models import Blog
from blog.serializers import BlogSerializer
from django.views.generic import TemplateView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class BlogListView(APIView):
    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all()

        current_page = request.GET.get("page", 1)

        paginator = Paginator(blogs, 9)

        try:
            blogs_page = paginator.page(current_page)
        except PageNotAnInteger:
            blogs_page = paginator.page(1)
        except EmptyPage:
            blogs_page = paginator.page(paginator.num_pages)

        serializer = BlogSerializer(blogs_page, many=True)

        pagination_data = {
            "current_page": int(current_page),
            "total_pages": paginator.num_pages,
            "has_next": blogs_page.has_next(),
            "has_previous": blogs_page.has_previous(),
            "next_page_number": (
                blogs_page.next_page_number() if blogs_page.has_next() else None
            ),
            "previous_page_number": (
                blogs_page.previous_page_number() if blogs_page.has_previous() else None
            ),
        }

        return Response(
            {"blogs": serializer.data, "pagination": pagination_data},
            status=status.HTTP_200_OK,
        )


class BlogPageView(TemplateView):
    template_name = "blogs-page.html"


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blog'
    slug_field = 'blog_seo_title'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        blog = self.object

        more_blogs = Blog.objects.filter(category=blog.category, is_active=True).exclude(id=blog.id)[:4]

        context['more_blogs'] = more_blogs
        return context