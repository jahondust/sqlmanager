from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User

UserAdmin.fieldsets += (
    (None, {'fields': ('queries',)}),
)

admin.site.register(User, UserAdmin)

