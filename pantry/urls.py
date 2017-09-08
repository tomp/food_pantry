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
from . import views
import clients.views

from pantry.admin import admin_site


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/?', flatpage, {'url': '/about/'}, name='about'),
    url(r'^stats/', flatpage, {'url': '/stats/'}, name='stats'),
    url(r'^visits/', flatpage, {'url': '/visits/'}, name='visits'),
    url(r'^clients/', flatpage, {'url': '/clients/'}, name='clients'),
    # url(r'^stats/', clients.views.stats, name='stats'),
    # url(r'^visits/', clients.views.visits, name='visits'),
    # url(r'^clients/', clients.views.summary, name='summary'),
    url(r'^admin/?', admin_site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
