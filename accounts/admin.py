
from django.contrib import admin

from .models import Account

# Register your models here.


class AccountInline(admin.ModelAdmin):
    model = Account
    can_delete = False

admin.site.register(Account, AccountInline)