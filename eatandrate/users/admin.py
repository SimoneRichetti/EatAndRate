from django.contrib import admin
from .models import UserProfile, OwnerProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(OwnerProfile)
