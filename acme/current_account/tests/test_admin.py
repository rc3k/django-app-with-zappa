from django.contrib.admin.sites import AdminSite
from django.test.client import RequestFactory

import pytest
from mock import patch

from ..admin import ApplicationAdmin, approve_application
from ..models import Application, ApplicationApproval, Account, AccountCard, STATUS_PENDING, STATUS_APPROVED

from .fixtures import *


@patch('acme.current_account.admin.approve_application')
@pytest.mark.django_db
def test_approve_application_called_when_status_changed_to_approved(mock_approve, applications, application_approver):
    application_1, application_2 = applications
    request = RequestFactory().request()
    request.user = application_approver
    application_1.status = STATUS_APPROVED
    ApplicationAdmin(
        model=Application, admin_site=AdminSite()
    ).save_model(request, application_1, None, True)
    assert mock_approve.call_count == 1
    mock_approve.assert_called_with(request, application_1)


@patch('acme.current_account.admin.approve_application')
@pytest.mark.django_db
def test_approve_application_not_called_when_status_changed_to_pending(mock_approve, applications, application_approver):
    application_1, application_2 = applications
    request = RequestFactory().request()
    request.user = application_approver
    application_2.status = STATUS_PENDING
    ApplicationAdmin(
        model=Application, admin_site=AdminSite()
    ).save_model(request, application_2, None, True)
    assert not mock_approve.called


@patch('acme.current_account.admin.issue_card_request')
@pytest.mark.django_db
def test_approve_application(mock_issue_card, applications, application_approver):
    application_1, application_2 = applications
    request = RequestFactory().request()
    request.user = application_approver
    application_1.status = STATUS_APPROVED
    approve_application(request, application_1)
    assert ApplicationApproval.objects.filter(application=application_1, user=application_approver).exists()
    assert Account.objects.filter(customer=application_1.customer).exists()
    account = Account.objects.get(customer=application_1.customer)
    assert AccountCard.objects.filter(account=account, initialised=False).exists()
    card = AccountCard.objects.get(account=account)

    # assert card issue task sent to queue (with whatever data might be required by the service endpoint?)
    assert mock_issue_card.delay.call_count == 1
    mock_issue_card.delay.assert_called_with({
        'application': {
            'id': 1,
            'url': 'http://testserver/api/application/1/',
            'customer': {
                'full_name': 'Geoff Biscuit',
                'mobile_number': '+447896123123',
                'address_line': '1 Jaffa Street',
                'postcode': 'JF1 GB2'
            },
            'status': 'approved',
            'status_text': 'Approved'
        },
        'account_id': account.id,
        'card_id': card.id
    })
