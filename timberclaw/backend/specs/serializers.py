from rest_framework import serializers

from .models import SpecDocument, SpecVersion


class SpecVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecVersion
        fields = ("id", "version_number", "scenario_view", "created_at")


class SpecDocumentSerializer(serializers.ModelSerializer):
    versions = SpecVersionSerializer(many=True, read_only=True)

    class Meta:
        model = SpecDocument
        fields = ("id", "title", "created_by", "created_at", "versions")
        read_only_fields = ("created_by", "created_at", "versions")


class SpecDocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecDocument
        fields = ("title",)
