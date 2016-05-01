from __future__ import unicode_literals
from django.db import models

class Breed(models.Model):
    breed = models.TextField()

    def __str__(self):
        return self.breed

    @classmethod
    def create(cls, breed):
        new_breed = cls(breed=breed)
        return new_breed


class Notes(models.Model):
    note = models.TextField()
    # i used quotes for the Dog class here because we have not instantiated it yet
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.note

    @classmethod
    def create(cls, text, dog):
        Note = cls(note=text, dog=dog)
        return Note

class Photos(models.Model):
    photo_url = models.TextField()
    dog = models.ForeignKey('Dog', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.photo_url

    @classmethod
    def create(cls, photo_url, dog):
        photo = cls(photo_url=photo_url, dog=dog)
        return photo


class Dog(models.Model):
    # consider setting default values to null
    pet_id = models.TextField()
    name = models.TextField()
    breeds = models.ManyToManyField(Breed)
    sex = models.TextField()
    age = models.TextField()
    contact_email = models.TextField()
    contact_phone = models.TextField()
    city = models.TextField()
    zip_code = models.TextField()
    size = models.TextField()
    description = models.TextField()
    adoptable = models.NullBooleanField(default=None)
    fosterable = models.NullBooleanField(default=None)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, pet_id, name, sex, age, contact_email, contact_phone, city, zip_code, size, description):
        dog = cls(pet_id=pet_id, name=name, sex=sex, age=age, contact_email=contact_email, contact_phone=contact_phone, city=city, zip_code=zip_code,size=size, description=description)
        return dog


class User(models.Model):
    # to be added immediately upon registration
    email = models.TextField(default='')
    # to be added after registration
    favorites = models.ManyToManyField(Dog, default=None)

    def __str__(self):
        return self.email

    @classmethod
    def create(cls, email):
        user = cls(email=email)
        return user
