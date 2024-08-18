from rest_framework import serializers
from content.models import Gallery


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        exclude = ["id"]

    def create(self, validated_data):
        return Gallery.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)