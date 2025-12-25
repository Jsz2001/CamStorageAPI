from django.http import request
from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserCameraSerializer, BrandListerSerializer

from .models import Camera, Brand, Gear
from .relations import MultipleHyperlinkedIdentityField


class BrandSerializer(serializers.ModelSerializer):
    brand_detail_url = MultipleHyperlinkedIdentityField(
        view_name='brand-detail',
        lookup_fields = (
            ('user.username', 'username'), 
            ('name', 'name')
        ), 
        read_only=True
    )
    lister = BrandListerSerializer(source='user', read_only=True)
    camera_count = serializers.IntegerField(source="brand_camera_count", read_only=True)
    gear_count = serializers.IntegerField(source="brand_gear_count", read_only=True)
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
    
    def create(self, validated_data):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required to create a brand.")

        brand_name = (validated_data.get("name") or "").strip()
        if not brand_name:
            raise serializers.ValidationError({"name": "Brand name is required."})

        website = validated_data.get("website")

        brand, created = Brand.objects.get_or_create(
            user=user,
            name=brand_name,
            defaults={"website": website},
        )

        # Optional: if brand already exists but website is empty, fill it once
        if not created and website and not brand.website:
            brand.website = website
            brand.save(update_fields=["website"])

        return brand
    

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
        request = self.context.get("request")
        user = getattr(request, "user", None)

        brand_data = validated_data.pop("brand", None)
        brand_obj = None

        if brand_data and brand_data.get("name"):
            brand_name = (brand_data.get("name") or "").strip()
            website = brand_data.get("website")

            brand_obj, created = Brand.objects.get_or_create(
                user=user,
                name=brand_name,
                defaults={"website": website},
            )

            # Optional: if user already had it, update website if they supplied one
            if website and brand_obj.website != website:
                brand_obj.website = website
                brand_obj.save()
        
        validated_data["brand"] = brand_obj
        return Camera.objects.create(**validated_data)



        # brand = validated_data.pop('brand', None)
        # if brand['name'] is None:
        #     return Camera.objects.create(**validated_data)
        # brand, created_bool = Brand.objects.get_or_create(name=brand['name'], defaults=brand)
        # validated_data['brand'] = brand
        # camera = Camera.objects.create(**validated_data)
        # return camera
    
    def get_detail_url(self, obj):
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("camera-detail", kwargs={"pk": obj.pk, "username": obj.user.username}, 
                       request=request)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Keep output as brand name only
        rep["brand"] = instance.brand.name if instance.brand else None
        return rep


class CameraDetailSerializer(serializers.ModelSerializer):
    owner = UserCameraSerializer(source='user', read_only=True)
    related_gear = serializers.SerializerMethodField()
    class Meta:
        model = Camera
        fields = [            
            'pk',
            'name',            
            'brand',
            'owner',
            'price',
            'note',
            'related_gear',
            ]
        
    def get_related_gear(self, obj):
        result = (obj.gears.values_list('name', 'gear_type'))
        return (result)
        
    def to_representation(self, instance):
        serializer_context={'request': self.context.get('request')}
        rep = super().to_representation(instance)
        rep['brand'] = BrandSerializer(instance.brand, context=serializer_context).data['name']
        return rep
    

class CamSlugRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            return Camera.objects.none()
        return Camera.objects.filter(user=request.user)


class GearSerializer(serializers.ModelSerializer):
    camera = CamSlugRelatedField(many=True, slug_field='name')
    owner = UserCameraSerializer(source='user', read_only=True)
    detail_url = serializers.SerializerMethodField(read_only=True)
    brand = BrandSerializer(required=False, allow_null=True)

    class Meta: 
        model = Gear
        fields = [
            'name',
            'brand',
            'owner',
            'detail_url',
            'gear_type',
            'note',
            'price',
            'quantity',
            'camera',
            ]

    def _get_or_create_brand(self, brand_data):
        if not brand_data:
            return None
        
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required to set brand.")

        brand_name = (brand_data.get("name") or "").strip()
        if not brand_name:
            return None

        website = (brand_data.get("website") or "").strip()

        # Brands are unique per user now (user + name)
        brand_obj, created = Brand.objects.get_or_create(
            user=user,
            name=brand_name,
            defaults={"website": website},
        )

        # Optional: update website if provided and changed
        if website and brand_obj.website != website:
            brand_obj.website = website
            brand_obj.save(update_fields=["website"])

        return brand_obj

    # def _get_brand(self, brand_name: str):
    #     request = self.context.get("request")
    #     user = getattr(request, "user", None)

    #     if not user or not user.is_authenticated:
    #         raise serializers.ValidationError("Authentication required to create a brand.")

    #     brand_name = (brand_name or "").strip()
    #     if not brand_name:
    #         return None

    #     brand, _ = Brand.objects.get_or_create(
    #         user=user,
    #         name=brand_name,
    #         defaults={"website": ""},
    #     )
    #     return brand

    def create(self, validated_data):
        brand_data = validated_data.pop("brand", None)
        brand_obj = self._get_or_create_brand(brand_data)
        validated_data["brand"] = brand_obj
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # allow updating brand through nested input
        if "brand" in validated_data:
            brand_data = validated_data.pop("brand", None)
            instance.brand = self._get_or_create_brand(brand_data)
        return super().update(instance, validated_data)
        
    def get_detail_url(self, obj):
        request = self.context.get('request') # self.request
        if request is None:
            return None
        return reverse("gear-detail", kwargs={"pk": obj.pk, "username": obj.user.username}, 
                       request=request)
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["brand"] = instance.brand.name if instance.brand else None
        return rep