from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics

from .models import UserData
from .serializers import UserSerializer, UserProfileSerializer
from .filters import UserFilter

from .mixins import ProfileQuerySetMixin


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'Auth_routes:',
        'api/login',
        'api/login/refresh',
        'api/Register',
        '---------------------------------------------',
        'User_routes:',
        'api/users',
        'api/users/<str:username>',
        '---------------------------------------------',
        'Camera_routes:',
        'api/users/<str:username>/cameras',
        'api/users/<str:username>/cameras/<int:pk>',
        '---------------------------------------------',
        'Brand_routes:',
        'api/users/<str:username>/brands',
        'api/users/<str:username>/brands/<str:brand-name>',
        'api/users/-/brands',
        '---------------------------------------------',
        'Gear_routes:',
        'api/users/<str:username>/gears',
        'api/users/<str:username>/gears/<int:pk>',
    ]

    return Response(routes)

@permission_classes([AllowAny])
class RegisterView(generics.CreateAPIView,):
    queryset = UserData.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class UserListView(UserFilter,
                   generics.ListAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileView(ProfileQuerySetMixin, generics.RetrieveUpdateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

