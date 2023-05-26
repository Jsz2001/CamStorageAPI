from rest_framework import generics
from rest_framework import filters

from api.mixins import UserQuerySetMixin
from api.filters import GearFilter, CameraFilter, BrandFilter

from .models import Camera, Brand, Gear
from .serializers import CameraSerializer, CameraDetailSerializer, BrandSerializer, GearSerializer

class CameraListCreateView(
    CameraFilter,
    UserQuerySetMixin,
    generics.ListCreateAPIView,):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)        


class CameraDetailView(
    UserQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,):
    queryset = Camera.objects.all()
    serializer_class = CameraDetailSerializer
    lookup_field = 'pk'


class UserBrandListCreateView(
    BrandFilter,
    UserQuerySetMixin,
    generics.ListCreateAPIView):
    '''
    See only your brands / list a new one
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    #lookup_field = 'name'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllBrandListCreateView(
    BrandFilter,
    generics.ListCreateAPIView):
    '''
    See all brands / list a new one
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    #lookup_field = 'name'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 


class BrandDetailView(
    UserQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'name'


class GearListCreateView(
    GearFilter,
    UserQuerySetMixin,
    generics.ListCreateAPIView,):
    queryset = Gear.objects.all()
    serializer_class = GearSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)   


class GearDetailView(
    UserQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,):
    queryset = Gear.objects.all()
    serializer_class = GearSerializer
    lookup_field = 'pk'