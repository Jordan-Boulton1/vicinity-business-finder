from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsReviewOwner

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing reviews.
    """
    queryset = Review.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ['business', 'rating', 'is_published']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer
    
    def get_permissions(self):
        """
        Custom permissions:
        - Anyone can view reviews
        - Authenticated users can create reviews
        - Only review owners can edit/delete their reviews
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsReviewOwner]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        # Check if user already reviewed this business
        business = serializer.validated_data['business']
        if Review.objects.filter(user=self.request.user, business=business).exists():
            raise ValidationError("You have already reviewed this business.")
        
        serializer.save(
            user=self.request.user,
            is_edited=False
        )

    def perform_update(self, serializer):
        serializer.save(is_edited=True)
