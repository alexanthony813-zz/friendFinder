from django.shortcuts import render
from django.http import HttpResponse
import urllib2
import json
import yaml
from dogs import models


def getString(obj):
    try:
        return obj['$t']
    except:
        return 'unavailable'


def saveDog(dog):
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
        breeds = dog['options']['option']
    except:
        breeds = []

    try:
        photos = dog['media']['photos']['photo']
    except:
        photos = []

    new_dog = models.Dog.create(pet_id, name, sex, age, contact_email, contact_phone, city, zip_code, size, description)
    new_dog.save()

    # get new dog primary id
    new_dog = models.Dog.objects.filter(pet_id=pet_id)[0]
    new_dog_id = new_dog.pk


    # many to many
    for breed in breeds:
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
    info = urllib2.urlopen('http://api.petfinder.com/pet.find?&format=json&key=e941c283e7da908741b97cf198cef9a8&location=33606&breed=dog&count=9').read()
    dogs = yaml.safe_load(info)['petfinder']['pets']['pet']

    for dog in dogs:
        # creates new entry if dog doesn't exist
        saveDog(dog)

    return render(request, 'users/home.html')
