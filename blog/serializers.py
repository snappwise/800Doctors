from rest_framework import serializers
from blog.models import blogCategories, Blog


class blogCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogCategories
        exclude = ["id"]

    def create(self, validated_data):
        return blogCategories.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ["id"]

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
