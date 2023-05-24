from django.urls import path

from . import views
from api.views import UserListView, UserProfileView

urlpatterns = [
    
        path('-/brands/', views.AllBrandListCreateView.as_view(), name='all-brand-list'),

        path('', UserListView.as_view(), name='user-list'),
        path('<str:username>/', UserProfileView.as_view(), name='user-detail'),        
        
        path('<str:username>/cameras/', views.CameraListCreateView.as_view(), name='camera-list'),
        path('<str:username>/cameras/<int:pk>/', views.CameraDetailView.as_view(), name='camera-detail'),

        path('<str:username>/brands/', views.UserBrandListCreateView.as_view(), name='user-brand-list'),
        path('<str:username>/brands/<str:name>/', views.BrandDetailView.as_view(), name='brand-detail'),

        path('<str:username>/gears/', views.GearListCreateView.as_view(), name='gear-list'),
        path('<str:username>/gears/<int:pk>/', views.GearDetailView.as_view(), name='gear-detail'),
]