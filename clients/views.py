from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Client, Dependent, Visit

class ClientSummaryView(TemplateView):
    template_name = "client_summary.html"

class ClientListView(LoginRequiredMixin, TemplateView):
    template_name = "client_list.html"

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        clients = []
        for client in Client.objects.all():
            clients.append({
                "id": client.id,
                "name": client.truncated_name(24),
                "url": "/clients/{}/".format(client.id),
                "regnum": client.id_number,
                "notes": client.truncated_notes(24),
            })
        context['clients'] = clients
        return context

class ClientDetailView(LoginRequiredMixin, DetailView):
    template_name = "client_detail.html"
    model = Client
