from rest_framework import filters


class UserFilter():
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['username']

class GearFilter():
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'gear_type', 'brand__name']
    ordering_fields = ['name', 'gear_type', 'brand']
    ordering = ['name']

class CameraFilter():
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'brand__name']
    ordering_fields = ['name', 'brand', 'price']
    ordering = ['name']

class BrandFilter():
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    