from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.template import RequestContext, loader

from .models import Drug
import requests
import json
# Create your views here.

def index(request):
	drug_list = Drug.objects.all()
	context = {'drug_list': drug_list}
	return render(request, 'drugs/index.html', context)