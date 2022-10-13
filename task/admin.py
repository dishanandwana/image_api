from django.contrib import admin

from task.models import Image, User,reimage

# Register your models here.
admin.site.register(User)
admin.site.register(Image)
admin.site.register(reimage)