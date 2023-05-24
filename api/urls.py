from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.getRoutes),

    path('register/', views.RegisterView.as_view(), name='sign_up'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('users/', views.UserListView.as_view(), name='user-list'),
    # path('users/<str:username>/', views.UserProfileView.as_view(), name='user-detail'),

]