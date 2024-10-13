from rest_framework import serializers
from blog.models import blogCategories, Blog


class blogCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogCategories
        fields = "__all__"

    def create(self, validated_data):
        return blogCategories.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BlogSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.category_name", read_only=True
    )

    class Meta:
        model = Blog
        fields = [
            "blog_seo_title",
            "blog_card_image",
            "category_name",  # Fetches the category name
            "blog_card_title",
            "blog_card_description",
            "blogger",
            "created_at",
        ]

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
