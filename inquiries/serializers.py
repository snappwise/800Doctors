from rest_framework import serializers
from inquiries.models import (
    generalEnquiry,
    healthcareEnquiry,
    serviceEnquiry,
)


class generalEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = generalEnquiry
        exclude = ["id"]

    def create(self, validated_data):
        return generalEnquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class healthcareEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = healthcareEnquiry
        exclude = ["id"]

    def create(self, validated_data):
        return healthcareEnquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class serviceEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = serviceEnquiry
        exclude = ["id"]

    def create(self, validated_data):
        return serviceEnquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
