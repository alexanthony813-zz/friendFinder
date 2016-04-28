from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import urllib2
import models

# gets all dogs
def index(request):
    dogs = models.Dog.filter()
    return render(request, 'includes/dogsnippet.html', {'dog_info': dogs})

def get_dog(request):
    dog_ids = request['dog_ids']
    dogs = models.Dog.filter(pk__in=dog_ids)
    return render(request, 'includes/dogsnippet.html', {'dog_info': dogs})
