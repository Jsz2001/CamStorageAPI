from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import UserData



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        ]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       username=validated_data['username'],
                                       first_name=validated_data['first_name'],
                                       last_name=validated_data['last_name'],
                                       )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field = 'username'
    )
    user_camera_url = serializers.SerializerMethodField(read_only=True)
    user_gear_url = serializers.SerializerMethodField(read_only=True)
    total_equipment_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserData
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',            
            'profile_url',
            'user_camera_url',
            'user_gear_url',
            'total_equipment_count'            
        ]

    def get_user_camera_url(self, obj):
        request = self.context.get('request') # self.request
        return reverse("camera-list", kwargs={"username": obj.username}, 
                        request=request)
    
    def get_user_gear_url(self, obj):
        request = self.context.get('request') # self.request
        return reverse("gear-list", kwargs={"username": obj.username}, 
                        request=request)
    
    def get_total_equipment_count(self, obj):
        cam_count = obj.camera_set.count()
        gear_count = obj.gear_set.count()
        total_count = cam_count + gear_count
        return total_count


class UserCameraSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)    
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field = 'username'
    )


class BrandListerSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)