from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
	fieldsets = UserAdmin.fieldsets + (
		('Additional Info', {'fields': ('phone', 'address')}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		('Additional Info', {'fields': ('phone', 'address')}),
	)

admin.site.register(CustomUser, CustomUserAdmin)

