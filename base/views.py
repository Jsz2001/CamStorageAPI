from rest_framework import generics

from api.mixins import UserQuerySetMixin
from api.filters import GearFilter, CameraFilter, BrandFilter

from .models import Camera, Brand, Gear
from .serializers import CameraSerializer, CameraDetailSerializer, BrandSerializer, GearSerializer


class CameraListCreateView(
    CameraFilter,
    UserQuerySetMixin,
    generics.ListCreateAPIView,):
    '''
    See all your cameras / store a new one
    (search cameras by name or brand)
    '''
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)        


class CameraDetailView(
    UserQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,):
    '''
    View specific camera / update camera information / delete camera
    (only cameras stored by user)
    '''
    queryset = Camera.objects.all()
    serializer_class = CameraDetailSerializer
    lookup_field = 'pk'


class UserBrandListCreateView(
    BrandFilter,
    UserQuerySetMixin,
    generics.ListCreateAPIView,):
    '''
    See only your brands / list a new one
    (search brands by name)
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllBrandListCreateView(
    BrandFilter,
    generics.ListCreateAPIView,):
    '''
    See all brands / list a new one
    (search brands by name)
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 


class BrandDetailView(
    UserQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,):
    '''
    View specific brand / update brand information / delete brand
    (only brands listed by user)
    '''
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'name'


class GearListCreateView(
    GearFilter,
    UserQuerySetMixin,
    generics.ListCreateAPIView,):
    '''
    See all your gear / store a new one
    (search gear by name, brand, or type of gear)
    '''
    queryset = Gear.objects.all()
    serializer_class = GearSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)   


class GearDetailView(
    UserQuerySetMixin,
    generics.RetrieveUpdateDestroyAPIView,):
    '''
    View specific gear / update gear information / delete gear
    (only gear stored by user)
    '''
    queryset = Gear.objects.all()
    serializer_class = GearSerializer
    lookup_field = 'pk'