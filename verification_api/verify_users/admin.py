from django.contrib import admin
from .models import Passport,Driving_License,PanCard
# Register your models here.
admin.site.register(Passport)
admin.site.register(Driving_License)
admin.site.register(PanCard)