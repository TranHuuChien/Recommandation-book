from django.contrib import admin
from .models.models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FavouriteBook)
admin.site.register(Rating)