from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Person, Client, Visit


class DependentInlineAdmin(admin.TabularInline):
    model = Person

@admin.register(Client)
class ClientAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'id_number', 'last_visit', 'notes')
    inlines = [DependentInlineAdmin]

@admin.register(Visit)
class VisitAdmin(SimpleHistoryAdmin):
    date_hierarchy = 'visited_at'
