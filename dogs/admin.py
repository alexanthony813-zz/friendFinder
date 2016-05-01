from django.contrib import admin
from dogs.models import Dog, Breed, Notes, Photos, User

# Register your models here.
admin.site.register(Dog)
admin.site.register(Breed)
admin.site.register(Notes)
admin.site.register(Photos)
admin.site.register(User)
