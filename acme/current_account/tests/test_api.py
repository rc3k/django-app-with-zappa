from django.urls import reverse

from rest_framework.test import APIClient
import pytest

from ..models import Application


@pytest.mark.django_db
def test_submit_application_success():
    assert Application.objects.all().count() == 0
    response = APIClient().post(reverse('application-list'), {
        'customer': {
            'full_name': 'Isobel Campbell',
            'mobile_number': '07912123123',
            'address_line': '43 Whatever',
            'postcode': 'BN12 1RB'
        }
    }, format='json')
    assert response.status_code == 201
    assert response.rendered_content == {
        'id': 1,
        'url': 'http://testserver/api/application/1/',
        'customer': {
            'full_name': 'Isobel Campbell',
            'mobile_number': '+447912123123',
            'address_line': '43 Whatever',
            'postcode': 'BN12 1RB'
        },
        'status': 'pending'
    }
    assert Application.objects.all().count() == 1


@pytest.mark.django_db
def test_load_payment():
    raise NotImplementedError('Not complete')


@pytest.mark.django_db
def test_list_transactions():
    raise NotImplementedError('Not complete')
