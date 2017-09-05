from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext, loader

def home(request):
    template = loader.get_template('home.html')
    context = RequestContext(request,{}).flatten()
    return HttpResponse(template.render(context))
