"""
Views for the product APIs
"""
from rest_framework import (
    viewsets,
    mixins,
    filters,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from asgiref.sync import sync_to_async
from django.db.models import QuerySet

from core.models import (
    Product,
    Tag,
    Category,
)
from product import serializers


class ProductViewSet(viewsets.ModelViewSet):
    """View for manage product APIs."""
    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'tags']
    search_fields = ['title', 'description']

    async def get_queryset(self):
        """Retrieve products for authenticated user."""
        queryset = await sync_to_async(list)(self.queryset.filter(user=self.request.user).order_by('-id'))
        return queryset

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ProductSerializer

        return self.serializer_class

    async def perform_create(self, serializer):
        """Create a new product."""
        await sync_to_async(serializer.save)(user=self.request.user)


class BaseProductAttrViewSet(mixins.DestroyModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """Base viewset for product attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    async def get_queryset(self):
        """Filter queryset to authenticated user."""
        queryset = await sync_to_async(list)(self.queryset.filter(user=self.request.user).order_by('-name'))
        return queryset


class TagViewSet(BaseProductAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class CategoryViewSet(BaseProductAttrViewSet):
    """Manage categories in the database."""
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
