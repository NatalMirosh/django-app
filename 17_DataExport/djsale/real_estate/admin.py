from django.contrib import admin

from .models import PropertyType, RoomCount, RealEstate, News


admin.site.register(PropertyType)
admin.site.register(RoomCount)
admin.site.register(RealEstate)
admin.site.register(News)