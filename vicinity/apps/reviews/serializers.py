from rest_framework import serializers
from .models import Review, ReviewImage
from apps.businesses.serializers import BusinessSerializer

class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image', 'caption', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    business_details = BusinessSerializer(source='business', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'business', 'business_details', 'user', 'user_name',
            'rating', 'title', 'content', 'is_published', 'is_edited',
            'created_at', 'updated_at', 'images'
        ]
        read_only_fields = ['user', 'is_edited', 'created_at', 'updated_at']

class ReviewCreateSerializer(ReviewSerializer):
    """Separate serializer for review creation with image uploads."""
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        review = Review.objects.create(**validated_data)

        # handle image uploads
        for image_data in images_data:
            ReviewImage.objects.create(
                review=review,
                image=image_data
            )

        return review
