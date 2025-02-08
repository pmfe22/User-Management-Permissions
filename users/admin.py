from django.contrib import admin
from .models import CustomUser

# Register the CustomUser model to admin
admin.site.register(CustomUser)
