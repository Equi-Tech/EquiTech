from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Account

# Register your models here.

class AccountAdminModel(ImportExportActionModelAdmin):
    list_editable = [
        'account_status',
        'account_balance',
        'kyc_submitted',
        'kyc_confirmed',
    ]
    list_display = [
        'user',
        'account_number',
        'account_status',
        'account_balance',
        'kyc_submitted',
        'kyc_confirmed',
    ]
    list_filter = [
        'account_status',
    ]


class KYCAdmin(ImportExportActionModelAdmin):
    search_fields = [
        "full_name",
    ]
    list_display = [
        'user',
        'full_name',
        'gender',
        'identity_type',
        'date_of_birth',
    ]

admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)