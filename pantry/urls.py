"""pantry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.flatpages.views import flatpage
from django.conf import settings
from django.contrib.auth import views as auth_views

from . import views
import clients.views

from pantry.admin import admin_site


urlpatterns = [
    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^about/', flatpage, {'url': '/about/'}, name='about'),
    url(r'^stats/', flatpage, {'url': '/stats/'}, name='stats'),
    url(r'^clients/(?P<pk>[0-9]+)/', clients.views.ClientDetailView.as_view(), name='client'),
    url(r'^clients/', clients.views.ClientListView.as_view(), name='clients'),
    url(r'^admin/?', admin_site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
