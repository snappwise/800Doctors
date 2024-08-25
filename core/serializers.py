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
        fields = '__all__'

    def create(self, validated_data):
        return Services.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class healthcareCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = healthcareCategories
        fields = '__all__'

    def create(self, validated_data):
        return healthcareCategories.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class healthcarePackagesSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.category_name", read_only=True)

    class Meta:
        model = healthcarePackages
        fields = '__all__'

    def create(self, validated_data):
        return healthcarePackages.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class FaqsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'

    def create(self, validated_data):
        return Faqs.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class TestimonialsSerializer(serializers.ModelSerializer):
    full_rating = serializers.IntegerField(read_only=True)
    half_rating = serializers.IntegerField(read_only=True)
    empty_rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Testimonials
        fields = '__all__'

    def create(self, validated_data):
        return Testimonials.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class JourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'

    def create(self, validated_data):
        return Journey.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)