from django.contrib import admin

from .models import Pet, Raca, Tag

admin.site.register(Raca)
admin.site.register(Tag)
admin.site.register(Pet)
