from django.contrib import admin

from .models import Customer, Account, AccountCard, ApplicationApproval, Application, STATUS_APPROVED, STATUS_PENDING
from .serializers import ApplicationSerializer
from .tasks import issue_card_request


def approve_application(request, application):
    ApplicationApproval.objects.create(
        application=application,
        user=request.user
    )
    account = Account.objects.create(
        customer=application.customer
    )
    card = AccountCard.objects.create(
        account=account
    )
    issue_card_request.delay({
        'application': ApplicationSerializer(application, context={'request': request}).data,
        'account_id': account.id,
        'card_id': card.id
    })


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if change:
            current_obj = self.get_object(request, obj.id)
            if obj.status == STATUS_APPROVED and current_obj.status == STATUS_PENDING:
                approve_application(request, obj)
        super().save_model(request, obj, form, change)


admin.site.register(Customer)
admin.site.register(Account)
