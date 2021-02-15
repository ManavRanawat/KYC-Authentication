from django.shortcuts import render

# Create your views here.
from .models import Passport,Driving_License,PanCard
from .serializers import PassportSerializer,Driving_LicenseSerializer,PanCardSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PassportList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        passport = Passport.objects.all()
        serializer = PassportSerializer(passport, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        passport = PassportSerializer(data=request.data)
        if passport.is_valid():
            passport.save()
            return Response(passport.data, status=status.HTTP_201_CREATED)
        return Response(passport.errors, status=status.HTTP_400_BAD_REQUEST)


class PassportDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Passport.objects.get(pk=pk)
        except Passport.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        passport = self.get_object(pk)
        serializer = PassportSerializer(passport)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        passport = self.get_object(pk)
        serializer = PassportSerializer(passport, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        passport = self.get_object(pk)
        passport.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Driving_LicenseList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        dl = Driving_License.objects.all()
        serializer = Driving_LicenseSerializer(dl, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        dl = Driving_LicenseSerializer(data=request.data)
        if dl.is_valid():
            dl.save()
            return Response(dl.data, status=status.HTTP_201_CREATED)
        return Response(dl.errors, status=status.HTTP_400_BAD_REQUEST)


class DrivingLicenseDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Driving_License.objects.get(pk=pk)
        except Driving_License.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dl = self.get_object(pk)
        serializer = Driving_LicenseSerializer(dl)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        dl = self.get_object(pk)
        serializer = Driving_LicenseSerializer(dl, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dl = self.get_object(pk)
        dl.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PanCardList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        pancard = PanCard.objects.all()
        serializer = PanCardSerializer(pancard, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        pancard = PanCardSerializer(data=request.data)
        if pancard.is_valid():
            # print("pancard :",pancard)
            pancard.save()
            # obj=Pancard.objects.get(name=pancard.name)
            return Response(pancard.data, status=status.HTTP_201_CREATED)
        return Response(pancard.errors, status=status.HTTP_400_BAD_REQUEST)


class PanCardDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return PanCard.objects.get(pk=pk)
        except PanCard.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        pancard = self.get_object(pk)
        serializer = PanCardSerializer(pancard)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pancard = self.get_object(pk)
        serializer = PanCardSerializer(pancard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pancard = self.get_object(pk)
        pancard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)