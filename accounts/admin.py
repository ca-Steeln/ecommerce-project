
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Account

# Register your models here.

class UserAccountInline(admin.StackedInline):
    model = Account
    can_delete = False

class AccountsUserAdmin(UserAdmin):
    def create_user_view(self, *args, **kwargs):
        self.inlines = []
        return super(AccountsUserAdmin, self).add_view(*args, **kwargs)

    def change_user_view(self, *args, **kwargs):
        self.inlines = [UserAccountInline]
        return super(AccountsUserAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)

