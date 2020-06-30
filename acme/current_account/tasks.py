from django.conf import settings

from celery import shared_task
import requests


@shared_task
def issue_card_request(request_data):
    external_partner_endpoint = getattr(settings, 'EXTERNAL_PARTNER_ENDPOINT', None)
    if external_partner_endpoint:
        return requests.post(
            external_partner_endpoint,
            request_data
        )
