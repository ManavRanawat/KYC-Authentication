from .models import Passport,Driving_License,PanCard
from rest_framework import serializers


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ['passport_no','date_of_issue','date_of_expiry','name']

class Driving_LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driving_License
        fields = ['dl_no','date_of_issue','date_of_expiry','name']

class PanCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PanCard
        fields = ['pancard_no','name']