from rest_framework import serializers
from .models import Business, BusinessImage

class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = ['id', 'image', 'caption', 'is_primary', 'created_at']


class BusinessSerializer(serializers.ModelSerializer):
    images = BusinessImageSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Business
        fields = [
            'id', 'name', 'owner', 'owner_name', 'category', 'description',
            'email', 'phone', 'website', 'address', 'city', 'state',
            'zip_code', 'latitude', 'longitude', 'hours_of_operation',
            'logo', 'average_rating', 'review_count', 'is_verified',
            'is_active', 'created_at', 'updated_at', 'images'
        ]
        read_only_fields = [
            'owner', 'average_rating', 'review_count', 
            'is_verified', 'created_at', 'updated_at'
        ]


class BusinessCreateSerializer(BusinessSerializer):
    """
    Separate serializer for business creation to handle image uploads.
    """
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        business = Business.objects.create(**validated_data)

        # handle image uploads
        for index, image_data in enumerate(images_data):
            BusinessImage.objects.create(
                business=business,
                image=image_data,
                is_primary=(index == 0)
            )

        return business
