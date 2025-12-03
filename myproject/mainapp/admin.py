from django.contrib import admin
from .models import Clients, Offices, Shipments

admin.site.register(Clients)
admin.site.register(Offices)
admin.site.register(Shipments)