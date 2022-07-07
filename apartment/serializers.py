from .models import Apartment


from rest_framework import serializers
from .models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        # fields = ["id", "manage_id", "apartment_add", "customer_name", "used", ]
        fields = "__all__"

    def validate(self, data):
        if data['manage_id'].strip() == "":
            raise serializers.ValidationError("MANAGE_ID is blank")
        if len(data['manage_id']) > 50:
            raise serializers.ValidationError("MANAGE_ID is too long")
        if len(data['customer_name']) > 50:
            raise serializers.ValidationError("CUSTOMER_NAME is too long")
        if len(data['apartment_add']) > 160:
            raise serializers.ValidationError("APARTMENT_ADD is too long")
        return data


class CreateApartmentSerializer(serializers.Serializer):
    manage_id = serializers.CharField(required=True)
    apartment_add = serializers.CharField(required=True)
    customer_name = serializers.CharField(required=True)
    created_company_cd = serializers.IntegerField()
    updated_company_cd = serializers.IntegerField()
    created_user_id = serializers.CharField()
    updated_user_id = serializers.CharField()
    created_user_name = serializers.CharField()
    updated_user_name = serializers.CharField()

    def create(self, validated_data):
        return Apartment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.manage_id = validated_data.get('manage_id', instance.manage_id)
        instance.apartment_add = validated_data.get('apartment_add', instance.apartment_add)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.created_company_cd = validated_data.get('created_company_cd', instance.created_company_cd)
        instance.updated_company_cd = validated_data.get('updated_company_cd', instance.updated_company_cd)
        instance.created_user_id = validated_data.get('created_user_id', instance.created_user_id)
        instance.updated_user_id = validated_data.get('updated_user_id', instance.updated_user_id)
        instance.created_user_name = validated_data.get('created_user_name', instance.created_user_name)
        instance.updated_user_name = validated_data.get('updated_user_name', instance.updated_user_name)
        # instance.save()
        return instance

    def validate(self, data):
        if data['manage_id'].strip() == "":
            raise serializers.ValidationError("MANAGE_ID is blank")
        if len(data['manage_id']) > 50:
            raise serializers.ValidationError("MANAGE_ID is too long")
        if len(data['customer_name']) > 50:
            raise serializers.ValidationError("CUSTOMER_NAME is too long")
        if len(data['apartment_add']) > 160:
            raise serializers.ValidationError("APARTMENT_ADD is too long")
        return data


class UpdateApartmentSerializer(serializers.Serializer):
    manage_id = serializers.CharField(required=True)
    apartment_add = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.manage_id = validated_data.get('manage_id', instance.manage_id)
        instance.apartment_add = validated_data.get('apartment_add', instance.apartment_add)
        return instance

