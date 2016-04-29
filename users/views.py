from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import json
import yaml

def index(request):
      return render(request, 'users/home.html')
