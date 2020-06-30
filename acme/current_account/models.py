from django.conf import settings
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

STATUS_PENDING = 'pending'

STATUS_APPROVED = 'approved'

APPLICATION_STATUSES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_APPROVED, 'Approved')
)


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    mobile_number = PhoneNumberField()
    address_line = models.CharField(max_length=255)
    postcode = models.CharField(max_length=8)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Application(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(choices=APPLICATION_STATUSES, max_length=12)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Application from {}'.format(self.customer.full_name)


class ApplicationApproval(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class AccountCard(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    initialised = models.BooleanField(default=False)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='GBP', default=0.00)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='GBP')
    created = models.DateTimeField(auto_now_add=True)
