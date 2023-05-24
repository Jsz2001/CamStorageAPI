from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserCameraSerializer, BrandListerSerializer

from .models import Camera, Brand, Gear
from .relations import MultipleHyperlinkedIdentityField


class BrandSerializer(serializers.ModelSerializer):
    brand_detail_url = MultipleHyperlinkedIdentityField(
        view_name='brand-detail',
        lookup_fields = (
            ('user', 'username'), 
            ('name', 'name')
        ), 
        read_only=True
    )
    lister = BrandListerSerializer(source='user', read_only=True)
    camera_count = serializers.SerializerMethodField(read_only=True)
    gear_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Brand
        fields = [
            'name',
            'website',
            'brand_detail_url',
            'camera_count',
            'gear_count',
            'lister',
        ]

    def get_camera_count(self, obj):
        count = obj.camera_set.count()
        return count
    
    def get_gear_count(self, obj):
        count = obj.gear_set.count()
        return count
    
    def create(self, validated_data):
        brand_name = validated_data.get('name')
        brand, created_bool = Brand.objects.get_or_create(name=brand_name, 
                                                          defaults=validated_data)
        return brand
    

# class BrandCameraSerializer(serializers.ModelSerializer):
#     lister = BrandListerSerializer(source='user', read_only=True)
#     class Meta:
#         model = Brand
#         fields = [
#             'name',
#             'website',
#             'lister',
#         ]
    
#     def create(self, validated_data):
#         brand_name = validated_data.get('name')
#         brand, created_bool = Brand.objects.get_or_create(name=brand_name, 
#                                                           defaults=validated_data)
#         return brand
    

class CameraSerializer(serializers.ModelSerializer):
    owner = UserCameraSerializer(source='user', read_only=True)
    brand = BrandSerializer()
    detail_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Camera
        fields = [
            'name',
            'owner',
            'detail_url',
            'price',
            'note',
            'brand',
        ]

    def create(self, validated_data):
        brand = validated_data.pop('brand', None)
        if brand['name'] is None:
            return Camera.objects.create(**validated_data)
        brand, created_bool = Brand.objects.get_or_create(name=brand['name'], defaults=brand)
        validated_data['brand'] = brand
        camera = Camera.objects.create(**validated_data)
        return camera
    
    def get_detail_url(self, obj):
        request = self.context.get('request') # self.request
        
        if request is None:
            return None
        return reverse("camera-detail", kwargs={"pk": obj.pk, "username": obj.user}, 
                       request=request)

    def to_representation(self, instance):
        serializer_context={'request': self.context.get('request')}
        rep = super().to_representation(instance)
        rep['brand'] = BrandSerializer(instance.brand, context=serializer_context).data['name']
        return rep


class CameraDetailSerializer(serializers.ModelSerializer):
    owner = UserCameraSerializer(source='user', read_only=True)
    class Meta:
        model = Camera
        fields = [            
            'pk',
            'name',            
            'brand',
            'owner',
            'price',
            'note',
            ]
        
    def to_representation(self, instance):
        serializer_context={'request': self.context.get('request')}
        rep = super().to_representation(instance)
        rep['brand'] = BrandSerializer(instance.brand, context=serializer_context).data['name']
        return rep
    

class CamSlugRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = Camera.objects.all()
        request = self.context.get('request', None)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset


class GearSerializer(serializers.ModelSerializer):
    camera = CamSlugRelatedField(many=True, slug_field='name')
    owner = UserCameraSerializer(source='user', read_only=True)
    class Meta: 
        model = Gear
        fields = [
            'name',
            'brand',
            'owner',
            'gear_type',
            'price',
            'quantity',
            'camera',
            ]
        
    def to_representation(self, instance):
        serializer_context={'request': self.context.get('request')}
        rep = super().to_representation(instance)
        rep['brand'] = BrandSerializer(instance.brand, context=serializer_context).data['name']
        return rep