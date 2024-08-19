from rest_framework import serializers
from inquiries.models import (
    generalEnquiry,
    healthcareEnquiry,
    serviceEnquiry,
)
from django.utils import timezone


class generalEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = generalEnquiry
        exclude = ["id"]

    def create(self, validated_data):
        return generalEnquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long."
            )
        return value


class healthcareEnquirySerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source="package.package_name", read_only=True)

    class Meta:
        model = healthcareEnquiry
        exclude = ["id"]

    def create(self, validated_data):
        return healthcareEnquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_package(self, value):
        if value is None:
            raise serializers.ValidationError("Package selection is required.")
        return value

    def validate(self, data):
        if data["pref_date"] < timezone.now().date():
            raise serializers.ValidationError("Preferred date cannot be in the past.")
        return data


class serviceEnquirySerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.service_name", read_only=True)

    class Meta:
        model = serviceEnquiry
        exclude = ["id"]

    def create(self, validated_data):
        return serviceEnquiry.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def validate_service(self, value):
        if value is None:
            raise serializers.ValidationError("Service selection is required.")
        return value

    def validate_message(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Message must be at least 10 characters long."
            )
        return value
