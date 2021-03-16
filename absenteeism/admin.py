from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Times, AbstractUser
# Register your models here.

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('cash', 'contact')}),
admin.site.register(User, UserAdmin)
admin.site.register(Times)