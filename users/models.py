from __future__ import unicode_literals

from django.db import models
from dogs import dog_models

# to sign up for user alerts
class AlertPreferences(models.Model):
    preference_field = models.TextField()

class User(models.Model):
    favorites = models.ForeignKey(dog_models.Dog, on_delete=models.CASCADE, default='none')
    friends = models.ForeignKey(dog_models.Dog, on_delete=models.CASCADE, default='none')
    preference = models.ForeignKey(AlertPreferences, on_delete=models.CASCADE, default='none')
