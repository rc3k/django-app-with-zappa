import pytest
from rest_framework.test import APIRequestFactory

from ..models import Application, STATUS_PENDING, STATUS_APPROVED
from ..serializers import ApplicationSerializer, CustomerSerializer

from .fixtures import *


@pytest.mark.django_db
def test_application_serializer_get_single(applications):
    request = APIRequestFactory().request()
    assert ApplicationSerializer(applications[0], context={'request': request}).data == {
        'id': applications[0].id,
        'customer': {
            'full_name': 'Geoff Biscuit',
            'mobile_number': '+447896123123',
            'address_line': '1 Jaffa Street',
            'postcode': 'JF1 GB2'
        },
        'status': STATUS_PENDING,
        'status_text': 'Pending',
        'url': 'http://testserver/api/application/{}/'.format(applications[0].id)
    }


@pytest.mark.django_db
def test_application_serializer_get_many(applications):
    request = APIRequestFactory().request()
    assert ApplicationSerializer(applications, many=True, context={'request': request}).data == [
        {
            'id': applications[0].id,
            'customer': {
                'full_name': 'Geoff Biscuit',
                'mobile_number': '+447896123123',
                'address_line': '1 Jaffa Street',
                'postcode': 'JF1 GB2'
            },
            'status': STATUS_PENDING,
            'status_text': 'Pending',
            'url': 'http://testserver/api/application/{}/'.format(applications[0].id)
        },
        {
            'id': applications[1].id,
            'customer': {
                'full_name': 'Frank Avocado',
                'mobile_number': '+447896123124',
                'address_line': '8 Cabbage Avenue',
                'postcode': 'BN1 1RT'
            },
            'status': STATUS_APPROVED,
            'status_text': 'Approved',
            'url': 'http://testserver/api/application/{}/'.format(applications[1].id)
        }
    ]


@pytest.mark.django_db
def test_application_serializer_create(applications):
    serializer = ApplicationSerializer(data={
        'customer': {
            'full_name': 'Help me Rhonda',
            'mobile_number': '+447896789789',
            'address_line': '14 Summer Days',
            'postcode': 'BB1 1BB'
        },
    })
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.customer.full_name == 'Help me Rhonda'
    assert instance.customer.mobile_number == '+447896789789'
    assert instance.customer.address_line == '14 Summer Days'
    assert instance.customer.postcode == 'BB1 1BB'
    assert instance.status == STATUS_PENDING


@pytest.mark.django_db
def test_application_serializer_update(applications):
    serializer = ApplicationSerializer(applications[0], data={
        'customer': {
            'full_name': 'Surfing Safari',
            'address_line': '13 The Mews',
        },
        'status': STATUS_APPROVED
    }, partial=True)
    assert serializer.is_valid()
    instance = serializer.save()
    assert instance.id == applications[0].id
    assert instance.customer.full_name == 'Surfing Safari'
    assert instance.customer.mobile_number == '+447896123123'
    assert instance.customer.address_line == '13 The Mews'
    assert instance.customer.postcode == 'JF1 GB2'
    assert instance.status == STATUS_APPROVED


@pytest.mark.django_db
def test_customer_serializer_create_invalid_mobile_number(applications):
    serializer = CustomerSerializer(data={
        'full_name': 'Help me Rhonda',
        'mobile_number': 'Invalid',
        'address_line': '14 Summer Days',
        'postcode': 'BB1 1BB'
    })
    assert not serializer.is_valid()
    assert 'mobile_number' in serializer.errors
    assert len(serializer.errors['mobile_number']) == 1
    assert serializer.errors['mobile_number'][0] == 'The phone number entered is not valid.'
    assert serializer.errors['mobile_number'][0].code == 'invalid_phone_number'


@pytest.mark.django_db
def test_customer_serializer_create_invalid_postcode(applications):
    serializer = CustomerSerializer(data={
        'full_name': 'Help me Rhonda',
        'mobile_number': '+447896789789',
        'address_line': '14 Summer Days',
        'postcode': '123 1BB'
    })
    assert not serializer.is_valid()
    assert 'postcode' in serializer.errors
    assert len(serializer.errors['postcode']) == 1
    assert serializer.errors['postcode'][0] == 'The postcode entered is not valid.'
    assert serializer.errors['postcode'][0].code == 'invalid_postcode'


@pytest.mark.django_db
def test_customer_serializer_create_empty_fields(applications):
    serializer = CustomerSerializer(data={
        'full_name': '',
        'mobile_number': '',
        'address_line': '',
        'postcode': ''
    })
    assert not serializer.is_valid()
    for field in [
        'full_name',
        'mobile_number',
        'address_line',
        'postcode'
    ]:
        assert field in serializer.errors
        assert len(serializer.errors[field]) == 1
        assert serializer.errors[field][0] == 'This field may not be blank.'
        assert serializer.errors[field][0].code == 'blank'
