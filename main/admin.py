from django.contrib import admin
from .models import ProfileDB, PostDB


# Register your models here.
admin.site.register(ProfileDB),
admin.site.register(PostDB)