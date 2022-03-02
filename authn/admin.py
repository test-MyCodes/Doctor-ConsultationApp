from django.contrib import admin

from authn.models import Profile, userdetails

# Register your models here.
admin.site.register(userdetails)
admin.site.register(Profile)