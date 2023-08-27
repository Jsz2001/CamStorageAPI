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
    '''
    All avaiable routes to access/interact with resources
    See 
    '''
    routes = [
        'Auth_routes:',
        'login',
        'login/refresh',
        'register',
        '---------------------------------------------',
        'User_routes:',
        'users',
        'users/<str:username>',
        '---------------------------------------------',
        'Camera_routes:',
        'users/<str:username>/cameras',
        'users/<str:username>/cameras/<int:pk>',
        '---------------------------------------------',
        'Brand_routes:',
        'users/<str:username>/brands',
        'users/<str:username>/brands/<str:brand-name>',
        'users/-/brands',
        '---------------------------------------------',
        'Gear_routes:',
        'users/<str:username>/gears',
        'users/<str:username>/gears/<int:pk>',
    ]

    return Response(routes)

@permission_classes([AllowAny])
class RegisterView(generics.CreateAPIView,):
    '''
    Register as a user of CamStorageAPI
    '''
    queryset = UserData.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class UserListView(UserFilter,
                   generics.ListAPIView):
    '''
    See all registered users
    (search users by username, first name, or last name)
    '''
    queryset = UserData.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileView(ProfileQuerySetMixin, generics.RetrieveUpdateAPIView):
    '''
    View your profile / update user information
    '''
    queryset = UserData.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

