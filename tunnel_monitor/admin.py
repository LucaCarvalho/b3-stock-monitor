import imp
from django.contrib import admin
from .models import Tunnel, PriceLog

# Register your models here.

admin.site.register(Tunnel)
admin.site.register(PriceLog)