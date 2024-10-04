from django.contrib import admin
from .models import Breed, Kitten, Rating

# Регистрируем модель Breed в админке
admin.site.register(Breed)
admin.site.register(Kitten)
admin.site.register(Rating)