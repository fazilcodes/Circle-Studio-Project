from django.contrib import admin
from .models import ProfileDB, PostDB, LikepostDB, FollowerDB


# Register your models here.
admin.site.register(ProfileDB),
admin.site.register(PostDB),
admin.site.register(LikepostDB),
admin.site.register(FollowerDB)