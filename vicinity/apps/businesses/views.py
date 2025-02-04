from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Business
from .serializers import BusinessSerializer, BusinessCreateSerializer
from .permissions import IsOwnerOrReadOnly

# Create your views here.

class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing businesses.
    """
    queryset = Business.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['category', 'city', 'state', 'is_verified']
    search_fields = ['name', 'description', 'address']
    ordering_fields = ['name', 'created_at', 'average_rating', 'review_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return BusinessCreateSerializer
        return BusinessSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def nearby(self, request, pk=None):
        """Find nearby businesses within a certain radius."""
        business = self.get_object()
        radius = float(request.query_params.get('radius', 5.0)) # radius is in kilometers

        # nearby query using distance calculation
        nearby = Business.objects.filter(
            '''
            SELECT *,
                (6371 * acos(cos(radians(%s)) * cos(radians(latitude)) *
                cos(radians(longitude) - radians(%s)) +
                sin(radians(%s)) * sin(radians(latitude)))) AS distance
            FROM businesses_business
            WHERE id != %s
            HAVING distance < %s
            ORDER BY distance
            LIMIT 10
        ''', [business.latitude, business.longitude,
              business.latitude, business.id, radius])
        
        serializer = BusinessSerializer(nearby, many=True)
        return Response(serializer.data)
