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
    blogger_first_name = serializers.CharField(source='blogger.first_name', read_only=True)
    blogger_last_name = serializers.CharField(source='blogger.last_name', read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
