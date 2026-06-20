from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Context, ContextProfile, Policy, RequesterType

admin.site.register(Context)
admin.site.register(ContextProfile)
admin.site.register(RequesterType)
admin.site.register(Policy)
