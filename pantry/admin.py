from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage


class PantryAdminSite(admin.AdminSite):
    site_header = "Food Pantry Administration"

admin_site = PantryAdminSite(name='pantry_admin')

admin_site.register(FlatPage, FlatPageAdmin)
admin_site.register(User, UserAdmin)

