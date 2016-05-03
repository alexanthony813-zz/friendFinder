from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from friendFinder import settings
from django.contrib.auth.decorators import login_required
import urllib2
import models
import yaml
import re

def getString(obj):
    try:
        return obj['$t']
    except:
        return 'unavailable'

def login(request):
    # next = request.GET.get('next', '/home/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, 'dogs/login.html', {'redirect_to': '/'})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

def saveDog(dog, zip_to_search):
    # prevents duplication
    if len(models.Dog.objects.filter(pet_id=getString(dog['id'])))>0:
        return

    # ends save if no pictures
    try:
        photos = dog['media']['photos']['photo']
        profile_photo_url = getString(photos[0])
    except:
        return

    pet_id = getString(dog['id'])
    name = getString(dog['name'])
    age = getString(dog['age'])
    description = getString(dog['description'])

    sex = getString(dog['sex'])
    if sex == 'M':
        sex = 'Male'
    else:
        sex = 'Female'

    size = getString(dog['size'])
    if size == 'S':
        size = 'Small'
    elif size =='L':
        size = 'Large'
    else:
        size = 'Medium'

    try:
        contact_email = getString(dog['contact']['email'])
    except:
        contact_email = 'unavailable'

    try:
        contact_phone = getString(dog['contact']['phone'])
    except:
        contact_phone = 'unavailable'

    try:
        city = getString(dog['contact']['city'])
    except:
        city = 'unavailable'

    try:
        zip_code = getString(dog['contact']['zip_code'])
    except:
        zip_code = zip_to_search

    try:
        notes = dog['options']['option']
    except:
        notes = []

    try:
        breeds = dog['breeds']['breed']
    except:
        breeds = []


    new_dog = models.Dog.create(pet_id, name, sex, age, contact_email, contact_phone, city, zip_code, size, description, profile_photo_url)
    new_dog.save()

    # get new dog primary id
    new_dog = models.Dog.objects.filter(pet_id=pet_id)[0]
    new_dog_id = new_dog.pk


    # many to many
    for breed in breeds:
        if breed == 'unavailable':
            breed = 'Mixed'
        # check to see if breed exists first
        new_breed = models.Breed.create(getString(breed))
        new_breed.save()
        # get new breed primary id
        new_breed = models.Breed.objects.filter(breed=getString(breed))[0]
        new_breed_id = new_breed.pk

        new_dog.breeds.add(new_breed_id)
        new_dog.save()

    # these two are one to many. can be queried later from join with foreign key from respective tables
    for note in notes:
        new_note = models.Notes.create(getString(note), new_dog)
        new_note.save()

    for photo in photos:
        new_photo = models.Photos.create(getString(photo), new_dog)
        new_photo.save()

    new_dog.save()



def index(request):
    zip_to_search = request.GET.get('zip_code')

    try:
        int(zip_to_search)
        if len(zip_to_search) == 5:
            url = 'http://api.petfinder.com/pet.find?&format=json&key=e941c283e7da908741b97cf198cef9a8&location=%s&breed=dog&count=10' % zip_to_search
            info = urllib2.urlopen(url).read()
            try:
                dogs = yaml.safe_load(info)['petfinder']['pets']['pet']
                for dog in dogs:
                    saveDog(dog, zip_to_search)
            except:
                pass
            all_dogs = models.Dog.objects.filter(zip_code=zip_to_search)
    except:
        all_dogs = models.Dog.objects.all()

    return render(request, 'dogs/header.html', {'dogs': all_dogs})
