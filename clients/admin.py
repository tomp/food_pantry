from django.contrib import admin
from .models import Dependent, Client, Visit


class DependentInlineAdmin(admin.TabularInline):
    model = Dependent
    fk_name = 'dependent_on'
    extra = 1

class VisitInlineAdmin(admin.TabularInline):
    model = Visit
    fk_name = 'client'
    readonly_fields = ['visited_at', 'picked_up_by']
    show_change_link = True
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'id_number', 'last_visit', 'notes')
    inlines = [VisitInlineAdmin, DependentInlineAdmin]

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    date_hierarchy = 'visited_at'
