
from django.contrib import admin
from .models import CustomUser
# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class CustomUserInline(admin.StackedInline):
    model = CustomUser

class CustomUserAdmin(UserAdmin):
    def create_user_view(self, *args, **kwargs):
        self.inlines = []
        return super(CustomUserAdmin, self).add_view(*args, **kwargs)

    def change_user_view(self, *args, **kwargs):
        self.inlines = [CustomUserAdmin]
        return super(CustomUserAdmin, self).change_view(*args, **kwargs)


admin.site.register(CustomUser, CustomUserAdmin)

