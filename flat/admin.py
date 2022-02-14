from django.contrib import admin

from .models import Flat, Photo, Renting

admin.site.register(Flat)
admin.site.register(Renting)
admin.site.register(Photo)
