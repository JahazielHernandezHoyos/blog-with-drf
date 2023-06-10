from rest_framework import serializers
from django.utils import timezone

class CustomSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CustomSerializer, self).get_field_names(
            declared_fields, info
        )

        if getattr(self.Meta, "extra_fields", None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class EmptySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

def calculate_age(birth_date):
    today = timezone.now()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))