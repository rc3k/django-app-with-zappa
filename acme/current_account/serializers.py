from postcode_validator_uk.exceptions import InvalidPostcode
from postcode_validator_uk.validators import UKPostcode
from rest_framework import serializers

from .models import Application, Customer, STATUS_PENDING, APPLICATION_STATUSES


class CustomerSerializer(serializers.ModelSerializer):

    def validate_postcode(self, value):
        postcode = UKPostcode(value)
        try:
            postcode.validate()
            return postcode.validated_postcode
        except InvalidPostcode:
            raise serializers.ValidationError('The postcode entered is not valid.', code='invalid_postcode')

    class Meta:
        model = Customer
        fields = (
            'full_name',
            'mobile_number',
            'address_line',
            'postcode'
        )


class ApplicationSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default=STATUS_PENDING)
    status_text = serializers.SerializerMethodField()
    customer = CustomerSerializer()

    def get_status_text(self, instance):
        return dict(APPLICATION_STATUSES)[instance.status]

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data['customer'])
        return Application.objects.create(
            status=STATUS_PENDING,
            customer=customer
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data['customer'].items():
            setattr(instance.customer, attr, value)
        instance.customer.save()
        if 'status' in validated_data:
            instance.status=validated_data['status']
        instance.save()
        return instance

    class Meta:
        model = Application
        fields = (
            'id',
            'url',
            'customer',
            'status',
            'status_text',
        )


class AccountSerializer(serializers.ModelSerializer):
    pass
