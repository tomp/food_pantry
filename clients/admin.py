from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Person, Client, Household, Visit

admin.site.register(Person, SimpleHistoryAdmin)
admin.site.register(Client, SimpleHistoryAdmin)
admin.site.register(Household, SimpleHistoryAdmin)
admin.site.register(Visit, SimpleHistoryAdmin)
