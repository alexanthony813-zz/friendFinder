from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from friendFinder import settings
from django.contrib.auth.decorators import login_required
import urllib2
import models
import yaml

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

def saveDog(dog):
    print dog
    # prevents duplication
    if len(models.Dog.objects.filter(pet_id=getString(dog['id'])))>0:
        return

    pet_id = getString(dog['id'])
    name = getString(dog['name'])
    sex = getString(dog['sex'])
    age = getString(dog['age'])
    size = getString(dog['size'])
    description = getString(dog['description'])

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
        zip_code = 'unavailable'

    try:
        notes = dog['options']['option']
    except:
        notes = []

    try:
        breeds = dog['breeds']['breed']
    except:
        breeds = []

    try:
        photos = dog['media']['photos']['photo']
        profile_photo_url = getString(photos[0])
    except:
        photos = []
        profile_photo_url = 'data:image/png;base64,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'

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
    info = urllib2.urlopen('http://api.petfinder.com/pet.find?&format=json&key=e941c283e7da908741b97cf198cef9a8&location=33602&breed=dog&count=9').read()
    dogs = yaml.safe_load(info)['petfinder']['pets']['pet']

    for dog in dogs:
        # creates new entry if dog doesn't exist
        saveDog(dog)

    all_dogs = models.Dog.objects.all()

    return render(request, 'dogs/header.html', {'dogs': all_dogs})
