from rest_framework import serializers
from core.models import (
    Services,
    healthcareCategories,
    healthcarePackages,
    Faqs,
    Testimonials,
    Journey,
)


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        exclude = ["id"]

    def create(self, validated_data):
        return Services.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class healthcareCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = healthcareCategories
        exclude = ["id"]

    def create(self, validated_data):
        return healthcareCategories.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class healthcarePackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = healthcarePackages
        exclude = ["id"]

    def create(self, validated_data):
        return healthcarePackages.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class FaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        exclude = ["id"]

    def create(self, validated_data):
        return Faqs.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class TestimonialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonials
        exclude = ["id"]

    def create(self, validated_data):
        return Testimonials.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        exclude = ["id"]

    def create(self, validated_data):
        return Journey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
