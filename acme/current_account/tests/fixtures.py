from django.contrib.auth import get_user_model

import pytest

from ..models import Application, Customer, STATUS_PENDING, STATUS_APPROVED


@pytest.fixture
def customers():
    customer_1 = Customer.objects.create(
        full_name='Geoff Biscuit',
        mobile_number='07896123123',
        address_line='1 Jaffa Street',
        postcode='JF1 GB2'
    )
    customer_2 = Customer.objects.create(
        full_name='Frank Avocado',
        mobile_number='07896123124',
        address_line='8 Cabbage Avenue',
        postcode='BN1 1RT'
    )
    return [customer_1, customer_2]


@pytest.fixture
def applications(customers):
    customer_1, customer_2 = customers
    application_1 = Application.objects.create(
        customer=customer_1,
        status=STATUS_PENDING
    )
    application_2 = Application.objects.create(
        customer=customer_2,
        status=STATUS_APPROVED
    )
    return [application_1, application_2]


@pytest.fixture
def application_approver():
    return get_user_model().objects.create(
        username='approver'
    )
