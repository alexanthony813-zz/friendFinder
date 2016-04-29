from __future__ import unicode_literals

from django.db import models
import dogs

# to sign up for user alerts
class Preference(models.Model):
    adopter = models.NullBooleanField(default=None)
    fosterer = models.NullBooleanField(default=None)
    breed = models.TextField(default='')
    size = models.TextField(default='')
    age = models.TextField(default='')
    zip_code = models.TextField(default='')
    city = models.TextField(default='')
    paragraph = models.TextField(default='')


class User(models.Model):
    # to be added immediately upon registration
    email = models.TextField(default='')
    preferences = models.ForeignKey(Preference, on_delete=models.CASCADE, default=None)
    # to be added after registration
    # favorites = models.ForeignKey(dogs.models.Dog, on_delete=models.CASCADE, default=None)

    @classmethod
    def create(clas, email, preferences):
        user = cls(email=email, preferences=preferences)
        return user
