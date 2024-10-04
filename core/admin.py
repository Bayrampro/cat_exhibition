from django.contrib import admin
from .models import Cat, Kind, Rating

admin.site.register(Cat)
admin.site.register(Kind)
admin.site.register(Rating)
